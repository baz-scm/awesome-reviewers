"""Pillar 2 — isolation that actually isolates.

Each test asserts one property of the sandbox by trying to violate it: leak an
environment variable in, hang past the timeout, spawn a child that outlives its
parent, allocate past the memory cap, or write a secret to stdout and have it
persisted.
"""

from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path
from unittest import mock

from awesome_harness.artifacts import EmptyArtifact, Store
from awesome_harness.cache import limits_from_config
from awesome_harness.errors import ExecutionError, StepTimeout, UsageError
from awesome_harness.execution import (
    ContainerSandbox,
    LocalSandbox,
    Limits,
    Output,
    Step,
    build_env,
    collect_outputs,
    env_fingerprint,
    ledger_body,
    select_sandbox,
    tool_fingerprints,
)
from awesome_harness.paths import ensure_dir

from .support import TempRepo


class TestStepParsing(unittest.TestCase):
    def test_argv_list_is_preserved(self) -> None:
        step = Step.parse({"id": "s", "run": ["echo", "a b"]})
        self.assertEqual(step.run, ("echo", "a b"))

    def test_string_command_is_split_without_a_shell(self) -> None:
        step = Step.parse({"id": "s", "run": "echo 'a b'"})
        self.assertEqual(step.run, ("echo", "a b"))

    def test_empty_command_is_refused(self) -> None:
        with self.assertRaises(UsageError):
            Step.parse({"id": "s", "run": []})

    def test_missing_fields_are_named(self) -> None:
        with self.assertRaises(UsageError) as caught:
            Step.parse({"id": "s"})
        self.assertIn("run", str(caught.exception))

    def test_identity_excludes_things_that_do_not_change_the_result(self) -> None:
        base = {"id": "s", "run": ["true"], "inputs": ["a"], "tools": ["python3 --version"]}
        quick = Step.parse({**base, "timeout_seconds": 5})
        slow = Step.parse({**base, "timeout_seconds": 500})
        self.assertEqual(quick.identity(), slow.identity(), "a timeout does not change the output")


class TestEnvironmentContract(unittest.TestCase):
    def test_only_allowlisted_names_are_passed(self) -> None:
        os.environ["HARNESS_TEST_LEAK"] = "should-not-appear"
        try:
            env = build_env(allow=["PATH"], fixed={"TZ": "UTC"}, step_env={}, home=Path("/tmp/h"))
        finally:
            del os.environ["HARNESS_TEST_LEAK"]
        self.assertNotIn("HARNESS_TEST_LEAK", env)
        self.assertEqual(env["TZ"], "UTC")

    def test_precedence_is_parent_then_fixed_then_step(self) -> None:
        os.environ["HARNESS_TEST_VAR"] = "from-parent"
        try:
            env = build_env(
                allow=["HARNESS_TEST_VAR"],
                fixed={"HARNESS_TEST_VAR": "from-fixed"},
                step_env={"HARNESS_TEST_VAR": "from-step"},
                home=Path("/tmp/h"),
            )
        finally:
            del os.environ["HARNESS_TEST_VAR"]
        self.assertEqual(env["HARNESS_TEST_VAR"], "from-step")

    def test_home_is_redirected_away_from_the_real_one(self) -> None:
        env = build_env(allow=["HOME"], fixed={}, step_env={}, home=Path("/tmp/run-home"))
        self.assertEqual(env["HOME"], "/tmp/run-home")

    def test_fingerprint_records_digests_not_values(self) -> None:
        prints = env_fingerprint({"TOKEN": "super-secret-value"})
        self.assertNotIn("super-secret-value", prints["TOKEN"])
        self.assertTrue(prints["TOKEN"].startswith("sha256:"))

    def test_ledger_body_never_carries_a_raw_env_value(self) -> None:
        step = Step(id="s", run=("echo", "--token=ghp_" + "a" * 36))
        body = ledger_body(step, {"DEPLOY_TOKEN": "raw-secret", "PATH": "/usr/bin"})
        serialized = repr(body)
        self.assertNotIn("raw-secret", serialized)
        self.assertNotIn("ghp_" + "a" * 36, serialized)
        self.assertIn("DEPLOY_TOKEN", body["env_names"])


class TestLocalSandbox(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.sandbox = LocalSandbox()
        self.run_dir = ensure_dir(self.root / "rundir")
        self.work = ensure_dir(self.root / "work")
        self.limits = Limits(memory_mb=0, cpu_seconds=30, wall_seconds=30, output_bytes=1 << 16)

    def _env(self) -> dict[str, str]:
        return build_env(
            allow=["PATH"], fixed={"TZ": "UTC", "LC_ALL": "C.UTF-8"}, step_env={}, home=self.run_dir
        )

    def _run(self, step: Step, **overrides):  # type: ignore[no-untyped-def]
        limits = Limits(**{**self.limits.__dict__, **overrides})
        return self.sandbox.execute(
            step, workdir=self.work, env=self._env(), limits=limits, run_dir=self.run_dir
        )

    def test_a_successful_step_reports_its_exit_code_and_output(self) -> None:
        result = self._run(Step(id="ok", run=("python3", "-c", "print('hello')")))
        self.assertEqual(result.exit_code, 0)
        self.assertIn("hello", result.stdout)

    def test_a_failing_step_is_reported_not_raised(self) -> None:
        result = self._run(Step(id="bad", run=("python3", "-c", "raise SystemExit(3)")))
        self.assertEqual(result.exit_code, 3)

    def test_undeclared_environment_variables_do_not_reach_the_step(self) -> None:
        os.environ["HARNESS_LEAK_CHECK"] = "leaked"
        try:
            result = self._run(
                Step(
                    id="env",
                    run=("python3", "-c", "import os;print('HARNESS_LEAK_CHECK' in os.environ)"),
                )
            )
        finally:
            del os.environ["HARNESS_LEAK_CHECK"]
        self.assertIn("False", result.stdout)

    def test_credentials_are_scrubbed_before_the_log_is_persisted(self) -> None:
        secret = "AKIAIOSFODNN7EXAMPLE"
        result = self._run(Step(id="leak", run=("python3", "-c", f"print('key={secret}')")))
        self.assertNotIn(secret, result.stdout)
        self.assertIn("aws-access-key-id", result.redactions)
        # And not merely in the returned string: the file on disk must be clean too.
        persisted = (self.run_dir / "leak.stdout").read_text(encoding="utf-8")
        self.assertNotIn(secret, persisted)

    def test_timeout_raises_and_kills_the_whole_process_group(self) -> None:
        # A child that outlives its parent is the leak a naive kill misses.
        script = (
            "import subprocess,sys,time;"
            "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)']);"
            "print(p.pid,flush=True);time.sleep(60)"
        )
        with self.assertRaises(StepTimeout):
            self._run(Step(id="hang", run=("python3", "-c", script), timeout_seconds=2.0))
        child_pid = int((self.run_dir / "hang.stdout").read_text(encoding="utf-8").split()[0])
        # Give the group kill a moment to land, then confirm the grandchild is gone.
        for _ in range(50):
            try:
                os.kill(child_pid, 0)
            except OSError:
                break
            import time as _time

            _time.sleep(0.1)
        else:
            self.fail(f"grandchild {child_pid} survived the timeout")

    def test_memory_limit_is_enforced(self) -> None:
        result = self._run(
            Step(id="hog", run=("python3", "-c", "b=bytearray(512*1024*1024);print(len(b))")),
            memory_mb=64,
        )
        self.assertNotEqual(result.exit_code, 0, "a 512MB allocation must fail under a 64MB cap")

    def test_missing_command_names_itself(self) -> None:
        with self.assertRaises(ExecutionError) as caught:
            self._run(Step(id="nope", run=("definitely-not-a-real-binary-xyz",)))
        self.assertIn("definitely-not-a-real-binary-xyz", str(caught.exception))

    def test_large_output_is_truncated_at_both_ends(self) -> None:
        script = "print('HEAD');print('x'*200000);print('TAIL')"
        result = self._run(Step(id="loud", run=("python3", "-c", script)), output_bytes=4096)
        self.assertTrue(result.truncated)
        self.assertIn("HEAD", result.stdout)
        self.assertIn("TAIL", result.stdout)
        self.assertIn("truncated", result.stdout)

    def test_isolation_report_admits_the_network_is_not_isolated(self) -> None:
        report = self.sandbox.isolation(Step(id="s", run=("true",)), self.limits)
        self.assertEqual(report["backend"], "local")
        self.assertIn("not isolated", str(report["network"]))

    def test_step_runs_in_the_worktree(self) -> None:
        (self.work / "marker.txt").write_text("here\n", encoding="utf-8")
        result = self._run(Step(id="cwd", run=("python3", "-c", "import os;print(os.listdir('.'))")))
        self.assertIn("marker.txt", result.stdout)


class TestOutputCollection(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.work = ensure_dir(self.root / "work")
        self.store = Store(self.ws.artifacts_dir)

    def test_globs_expand_in_sorted_order(self) -> None:
        for name in ("b.log", "a.log", "c.log"):
            (self.work / name).write_text("x\n", encoding="utf-8")
        step = Step(id="s", run=("true",), outputs=(Output(path="*.log"),))
        found = [p.name for _, p in collect_outputs(step, self.work)]
        self.assertEqual(found, ["a.log", "b.log", "c.log"])

    def test_a_missing_required_output_fails_by_name(self) -> None:
        step = Step(id="s", run=("true",), outputs=(Output(path="report.json"),))
        collected = collect_outputs(step, self.work)
        self.assertEqual(len(collected), 1)
        with self.assertRaises(EmptyArtifact):
            self.store.put_file(collected[0][1], name="report.json")

    def test_an_optional_output_may_be_absent(self) -> None:
        step = Step(id="s", run=("true",), outputs=(Output(path="maybe.json", optional=True),))
        self.assertEqual(collect_outputs(step, self.work), [])


class TestContainerIsolationIdentity(unittest.TestCase):
    """The image digest must not move under a run.

    An unmemoized probe answers None before the first `docker run` and a real digest
    afterwards, because running the step pulls the image. Two identical runs would then
    compute two different cache keys.
    """

    def test_the_digest_probe_runs_at_most_once(self) -> None:
        sandbox = ContainerSandbox("example/img:tag")
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="example/img@sha256:abc\n", stderr="")
        with mock.patch("awesome_harness.execution.subprocess.run", return_value=completed) as probe:
            first = sandbox.image_digest()
            second = sandbox.image_digest()
        self.assertEqual(first, "example/img@sha256:abc")
        self.assertEqual(second, first)
        self.assertEqual(probe.call_count, 1, "the probe must be memoized, not merely fast")

    def test_a_later_pull_cannot_change_the_answer(self) -> None:
        sandbox = ContainerSandbox("example/img:tag")
        absent = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="No such image")
        pulled = subprocess.CompletedProcess(args=[], returncode=0, stdout="example/img@sha256:abc\n", stderr="")
        with mock.patch("awesome_harness.execution.subprocess.run", side_effect=[absent, pulled]):
            self.assertIsNone(sandbox.image_digest())
            self.assertIsNone(sandbox.image_digest(), "a pull during the run must not move the identity")

    def test_an_absent_runtime_resolves_to_none_rather_than_raising(self) -> None:
        sandbox = ContainerSandbox("example/img:tag", runtime="definitely-not-a-runtime")
        self.assertIsNone(sandbox.image_digest())
        available, reason = sandbox.available()
        self.assertFalse(available)
        self.assertIn("not on PATH", reason)


class TestBackendSelection(unittest.TestCase):
    def test_local_is_explicit(self) -> None:
        sandbox, note = select_sandbox("local", "img")
        self.assertEqual(sandbox.name, "local")
        self.assertIn("configured", note)

    def test_auto_reports_which_backend_it_chose_and_why(self) -> None:
        sandbox, note = select_sandbox("auto", "python:3.11-slim")
        self.assertIn(sandbox.name, ("local", "container"))
        self.assertTrue(note.startswith("auto:"))
        if sandbox.name == "local":
            self.assertIn("container unavailable", note)

    def test_unknown_backend_is_refused(self) -> None:
        with self.assertRaises(UsageError):
            select_sandbox("podman-maybe", "img")


class TestToolFingerprints(TempRepo):
    def test_a_present_tool_is_fingerprinted(self) -> None:
        prints = tool_fingerprints(["python3 --version"], cwd=self.root, env=dict(os.environ))
        self.assertTrue(prints["python3 --version"].startswith("sha256:"))

    def test_an_absent_tool_is_recorded_not_skipped(self) -> None:
        # An absent compiler is a different cache key from a present one.
        prints = tool_fingerprints(["definitely-not-real-xyz --version"], cwd=self.root, env=dict(os.environ))
        self.assertIn("definitely-not-real-xyz --version", prints)

    def test_limits_come_from_config(self) -> None:
        limits = limits_from_config({"execution": {"memory_mb": 512, "timeout_seconds": 60}})
        self.assertEqual(limits.memory_mb, 512)
        self.assertEqual(limits.wall_seconds, 60)


if __name__ == "__main__":
    unittest.main()
