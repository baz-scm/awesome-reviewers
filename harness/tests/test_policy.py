"""Pillar 6 — every check gets a positive and a negative fixture.

A check with only a positive fixture is a check nobody has shown to be quiet on
correct code, and false positives are how gates get switched off. So each check here
is given code that should fire it and code that should not, and `test_every_check_is_covered`
fails if a new check ships without both.

Also tested: the anti-fiction guard. `policy build` must refuse a check whose corpus
slug does not resolve, and the real corpus must resolve every slug the registry
names — because a rule citing an instruction that does not exist enforces nothing
while looking exactly like one that does.
"""

from __future__ import annotations

import json
import unittest

from awesome_harness.errors import ConfigError, CorpusError, IntegrityError, UsageError
from awesome_harness.policy import (
    CHECKS,
    Corpus,
    Waiver,
    Waivers,
    advisory_bundle,
    build_context,
    build_pack,
    evaluate,
    load_pack,
    save_pack,
)
from awesome_harness.policy.checks import matches_selector
from awesome_harness.scm import Git

from .support import REAL_CORPUS, TempRepo


# Per check: a file that must produce a finding, and one that must not.
# (check id, path, offending source, compliant source)
FIXTURES: list[tuple[str, str, str, str]] = [
    (
        "AH001",
        "config.py",
        'AWS_KEY = "AKIAIOSFODNN7EXAMPLE"\n',
        'AWS_KEY = os.environ["AWS_KEY"]\n',
    ),
    (
        "AH002",
        ".github/workflows/ci.yml",
        "jobs:\n  b:\n    steps:\n      - uses: actions/checkout@main\n",
        "jobs:\n  b:\n    steps:\n      - uses: actions/checkout@" + "a" * 40 + "\n",
    ),
    (
        "AH003",
        ".github/workflows/perm.yml",
        "name: x\npermissions: write-all\njobs: {}\n",
        "name: x\npermissions:\n  contents: read\njobs: {}\n",
    ),
    (
        "AH004",
        "shellout.py",
        "import subprocess\ndef f(name):\n    subprocess.run(f'rm {name}', shell=True, timeout=5)\n",
        "import subprocess\ndef f(name):\n    subprocess.run(['rm', name], timeout=5)\n",
    ),
    (
        "AH005",
        "confine.py",
        "def ok(base_dir, candidate):\n    return str(candidate).startswith(str(base_dir))\n",
        "def ok(base_dir, candidate):\n    return candidate.resolve().is_relative_to(base_dir.resolve())\n",
    ),
    (
        "AH006",
        "unpack.py",
        "import tarfile\ndef f(t, d):\n    t.extractall(d)\n",
        "import tarfile\ndef f(t, d):\n    t.extractall(d, filter='data')\n",
    ),
    (
        "AH007",
        "swallow.py",
        "def f():\n    try:\n        g()\n    except:\n        pass\n",
        "def f():\n    try:\n        g()\n    except ValueError as exc:\n        raise RuntimeError('g failed') from exc\n",
    ),
    (
        "AH008",
        "fetch.py",
        "import requests\ndef f(u):\n    return requests.get(u)\n",
        "import requests\ndef f(u):\n    return requests.get(u, timeout=10)\n",
    ),
    (
        "AH009",
        "spawn.py",
        "import subprocess\ndef f():\n    return subprocess.run(['true'])\n",
        "import subprocess\ndef f():\n    return subprocess.run(['true'], timeout=30)\n",
    ),
    (
        "AH010",
        "settings.py",
        "import os\nDSN = os.environ['DATABASE_URL']\n",
        "import os\nDSN = os.environ.get('DATABASE_URL', 'sqlite://')\n",
    ),
    (
        "AH011",
        "audit.py",
        "import logging\ndef f(api_key):\n    logging.info('using %s', api_key)\n",
        "import logging\ndef f(api_key):\n    logging.info('using a key of %d chars', len(api_key))\n",
    ),
    (
        "AH012",
        "requirements.txt",
        "requests\n",
        "requests==2.32.3\n",
    ),
    (
        "AH013",
        "defaults.py",
        "def f(items=[]):\n    return items\n",
        "def f(items=None):\n    return items or []\n",
    ),
    (
        "AH014",
        "guard.py",
        "def f(x):\n    assert x > 0\n    return x\n",
        "def f(x):\n    if x <= 0:\n        raise ValueError('x must be positive')\n    return x\n",
    ),
    (
        "AH015",
        "Dockerfile",
        "FROM python:3.11.9-slim\nRUN echo hi\n",
        "FROM python:3.11.9-slim\nUSER 1000\nRUN echo hi\n",
    ),
    (
        "AH016",
        "Dockerfile.base",
        "FROM python:latest\nUSER 1000\n",
        "FROM python:3.11.9-slim\nUSER 1000\n",
    ),
    (
        "AH017",
        ".github/workflows/inj.yml",
        "permissions:\n  contents: read\njobs:\n  a:\n    steps:\n"
        "      - run: echo ${{ github.event.pull_request.title }}\n",
        # The compliant form puts the expression in `env:` and reads a shell variable.
        "permissions:\n  contents: read\njobs:\n  a:\n    steps:\n"
        '      - run: echo "$TITLE"\n        env:\n          TITLE: ${{ github.event.pull_request.title }}\n',
    ),
    (
        "AH018",
        "scripts/deploy.sh",
        "#!/bin/bash\necho deploying\n",
        "#!/bin/bash\nset -euo pipefail\necho deploying\n",
    ),
    (
        "AH019",
        "scripts/clean.sh",
        '#!/bin/bash\nset -euo pipefail\nrm -rf $TARGET_DIR\n',
        '#!/bin/bash\nset -euo pipefail\nrm -rf "${TARGET_DIR}"\n',
    ),
    (
        "AH020",
        "dyn.py",
        "def parse(text):\n    return eval(text)\n",
        "import json\n\n\ndef parse(text):\n    return json.loads(text)\n",
    ),
    (
        "AH021",
        "repo.py",
        "def get(session, key):\n    return session.query(User).filter_by(id=key).first()\n",
        "from sqlalchemy import select\n\n\ndef get(session, key):\n"
        "    return session.scalar(select(User).where(User.id == key))\n",
    ),
    (
        "AH022",
        "aio.py",
        "import time\n\n\nasync def wait():\n    time.sleep(1)\n",
        "import asyncio\n\n\nasync def wait():\n    await asyncio.sleep(1)\n",
    ),
    (
        "AH023",
        "svc.py",
        'import logging\n\nlogger = logging.getLogger(__name__)\n\n\ndef start():\n    print("starting")\n',
        'import logging\n\nlogger = logging.getLogger(__name__)\n\n\ndef start():\n    logger.info("starting")\n',
    ),
    (
        "AH024",
        "deploy/pod.yml",
        "spec:\n  containers:\n    - name: app\n      securityContext:\n        privileged: true\n",
        "spec:\n  containers:\n    - name: app\n      securityContext:\n"
        "        runAsNonRoot: true\n        allowPrivilegeEscalation: false\n",
    ),
    (
        "AH025",
        "package.json",
        '{\n  "dependencies": {\n    "left-pad": "^1.3.0"\n  }\n}\n',
        '{\n  "dependencies": {\n    "left-pad": "1.3.0"\n  }\n}\n',
    ),
    (
        "AH026",
        "srv.go",
        "func shutdown(c io.Closer) {\n\t_ = c.Close()\n}\n",
        "func shutdown(c io.Closer) error {\n\tif err := c.Close(); err != nil {\n"
        "\t\treturn fmt.Errorf(\"closing listener: %w\", err)\n\t}\n\treturn nil\n}\n",
    ),
    (
        "AH027",
        "scripts/tmp.sh",
        '#!/bin/bash\nset -euo pipefail\nworkdir="/tmp/app-$RANDOM"\n',
        '#!/bin/bash\nset -euo pipefail\nworkdir="$(mktemp -d /tmp/app-XXXXXX)"\n',
    ),
    (
        "AH028",
        ".github/workflows/prt.yml",
        "on: pull_request_target\npermissions:\n  contents: read\njobs:\n  a:\n    steps:\n"
        "      - uses: actions/checkout@" + "a" * 40 + "\n",
        "on: pull_request_target\npermissions:\n  contents: read\njobs:\n  a:\n    steps:\n"
        "      - uses: actions/checkout@" + "a" * 40 + "\n        with:\n          ref: refs/heads/main\n",
    ),
    (
        "AH029",
        "mod.ts",
        "export function parse(text: string) {\n  return eval(text);\n}\n",
        "export function parse(text: string) {\n  return JSON.parse(text);\n}\n",
    ),
    (
        "AH030",
        "nul.py",
        "def missing(value):\n    return value == None\n",
        "def missing(value):\n    return value is None\n",
    ),
    (
        "AH031",
        "tasks.py",
        "import asyncio\n\n\nasync def start(work):\n    asyncio.create_task(work())\n",
        "import asyncio\n\n\nasync def start(work):\n    task = asyncio.create_task(work())\n    await task\n",
    ),
    (
        "AH032",
        "Dockerfile.layers",
        "FROM python:3.11.9-slim\nUSER 1000\nCOPY . /app\nRUN pip install -r /app/requirements.txt\n",
        "FROM python:3.11.9-slim\nUSER 1000\nCOPY requirements.txt /app/\n"
        "RUN pip install -r /app/requirements.txt\nCOPY . /app\n",
    ),
    (
        "AH033",
        "log.ts",
        'export const trace = (m: string) => console.log(m);\n',
        'export const trace = (m: string) => console.debug(m);\n',
    ),
    (
        "AH034",
        "proc.py",
        'import subprocess\n\n\ndef build():\n    subprocess.run(["make"], timeout=60)\n',
        'import subprocess\n\n\ndef build():\n    subprocess.run(["make"], timeout=60, check=True)\n',
    ),
    (
        "AH035",
        "scripts/install.sh",
        "#!/bin/bash\nset -euo pipefail\ncurl -fsSL https://example.com/i.sh | sh\n",
        "#!/bin/bash\nset -euo pipefail\ncurl -fsSL -o i.sh https://example.com/i.sh\n"
        'echo "$EXPECTED_SHA  i.sh" | sha256sum -c -\nsh i.sh\n',
    ),
]


class TestChecks(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.git = Git(self.root)
        self.pack = build_pack(Corpus(self.corpus), name="all", limit=0)
        save_pack(self.ws.policy_dir, self.pack)

    def _findings(self, path: str, source: str) -> list:
        self.write(path, source)
        ctx = build_context(self.git, self.root, None)
        return evaluate(self.pack, ctx, threshold="info").findings

    def test_every_check_is_covered_by_a_fixture(self) -> None:
        covered = {check_id for check_id, *_ in FIXTURES}
        self.assertEqual(
            covered,
            set(CHECKS),
            "every registered check needs a positive and a negative fixture in FIXTURES",
        )

    def test_positive_fixtures_fire(self) -> None:
        for check_id, path, offending, _ in FIXTURES:
            with self.subTest(check=check_id):
                findings = self._findings(path, offending)
                fired = {f.check for f in findings}
                self.assertIn(check_id, fired, f"{check_id} did not fire on its own fixture: {findings}")
                (self.root / path).unlink()

    def test_negative_fixtures_stay_quiet(self) -> None:
        for check_id, path, _, compliant in FIXTURES:
            with self.subTest(check=check_id):
                findings = self._findings(path, compliant)
                fired = {f.check for f in findings}
                self.assertNotIn(
                    check_id, fired, f"{check_id} fired on compliant code: {[f.render() for f in findings]}"
                )
                (self.root / path).unlink()

    def test_findings_cite_a_resolvable_slug(self) -> None:
        corpus = Corpus(self.corpus)
        findings = self._findings("bad.py", "def f(x=[]):\n    return x\n")
        self.assertTrue(findings)
        for finding in findings:
            self.assertTrue(corpus.get(finding.slug).title, finding.slug)

    def test_branch_pinned_action_is_an_error_but_a_tag_is_a_warning(self) -> None:
        branch = self._findings(".github/workflows/a.yml", "steps:\n  - uses: x/y@main\n")
        (self.root / ".github/workflows/a.yml").unlink()
        tag = self._findings(".github/workflows/b.yml", "steps:\n  - uses: x/y@v4\n")
        self.assertEqual([f.severity for f in branch if f.check == "AH002"], ["error"])
        self.assertEqual([f.severity for f in tag if f.check == "AH002"], ["warning"])

    def test_local_actions_are_not_flagged(self) -> None:
        findings = self._findings(".github/workflows/c.yml", "steps:\n  - uses: ./.github/actions/build\n")
        self.assertNotIn("AH002", {f.check for f in findings})

    def test_syntax_error_is_a_note_not_a_silent_pass(self) -> None:
        self.write("broken.py", "def f(:\n")
        ctx = build_context(self.git, self.root, None)
        result = evaluate(self.pack, ctx, threshold="info")
        self.assertTrue(any("does not parse" in note for note in result.notes), result.notes)

    def test_only_added_lines_are_judged(self) -> None:
        self.write("legacy.py", "def f(items=[]):\n    return items\n")
        self.commit("pre-existing violation")
        self.write("legacy.py", "def f(items=[]):\n    return items\n\n\ndef g():\n    return 1\n")
        ctx = build_context(self.git, self.root, None)
        result = evaluate(self.pack, ctx, threshold="info")
        self.assertNotIn(
            "AH013",
            {f.check for f in result.findings},
            "a pre-existing violation must not be blamed on an unrelated change",
        )

    def test_the_summary_never_contradicts_the_verdict(self) -> None:
        # A warning below the threshold is reported but does not block. Counting it as
        # blocking produced "pass — 3 blocking findings", and a gate whose own summary
        # disagrees with its verdict does not get believed.
        from awesome_harness.policy import summary

        self.write("warn.py", "def f(x=[]):\n    return x\n")  # AH013, warning
        ctx = build_context(self.git, self.root, None)
        result = evaluate(self.pack, ctx, threshold="error")
        counts = summary(result)
        self.assertEqual(result.verdict, "pass")
        self.assertEqual(counts["blocking"], 0)
        self.assertGreater(counts["unsuppressed"], 0)
        self.assertGreaterEqual(counts["total"], counts["unsuppressed"])

    def test_a_finding_at_the_threshold_blocks_and_is_counted(self) -> None:
        from awesome_harness.policy import summary

        self.write("boom.py", "import subprocess\ndef f(n):\n    subprocess.run(f'rm {n}', shell=True, timeout=1)\n")
        ctx = build_context(self.git, self.root, None)
        result = evaluate(self.pack, ctx, threshold="error")
        self.assertEqual(result.verdict, "fail")
        self.assertEqual(summary(result)["blocking"], len(result.blocking))
        self.assertGreater(summary(result)["blocking"], 0)

    def test_fingerprint_survives_a_line_shift(self) -> None:
        first = self._findings("shift.py", "def f(x=[]):\n    return x\n")
        self.write("shift.py", "# a new comment\n# and another\ndef f(x=[]):\n    return x\n")
        ctx = build_context(self.git, self.root, None)
        second = evaluate(self.pack, ctx, threshold="info").findings
        by_check = lambda rows: {f.fingerprint for f in rows if f.check == "AH013"}  # noqa: E731
        self.assertEqual(by_check(first), by_check(second))
        self.assertNotEqual(
            [f.line for f in first if f.check == "AH013"],
            [f.line for f in second if f.check == "AH013"],
        )


class TestSuppression(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.git = Git(self.root)
        self.pack = build_pack(Corpus(self.corpus), name="all", limit=0)

    def _evaluate(self, *, waivers: Waivers | None = None, today: str = "2026-01-01"):  # type: ignore[no-untyped-def]
        ctx = build_context(self.git, self.root, None)
        return evaluate(self.pack, ctx, waivers=waivers, threshold="info", today=today)

    def test_inline_allow_with_a_reason_suppresses(self) -> None:
        self.write("s.py", "def f(x=[]):  # harness:allow AH013 - fixture for the suppression test\n    return x\n")
        finding = next(f for f in self._evaluate().findings if f.check == "AH013")
        self.assertFalse(finding.blocking)
        self.assertIn("fixture for the suppression test", finding.suppressed_by)

    def test_inline_allow_without_a_reason_does_not_suppress(self) -> None:
        self.write("s.py", "def f(x=[]):  # harness:allow AH013\n    return x\n")
        finding = next(f for f in self._evaluate().findings if f.check == "AH013")
        self.assertTrue(finding.blocking, "an unexplained suppression must not count")

    def test_the_allow_marker_must_be_on_the_line_or_the_one_above(self) -> None:
        # The window is two lines, so a wrapped multi-line justification puts the marker
        # out of reach. Documented by a test because it is the kind of thing that reads
        # as "suppression is broken" when it is really "the marker moved".
        self.write(
            "s.py",
            "# harness:allow AH013 - a reason on the wrong line\n"
            "# continuation of the reason\n"
            "def f(x=[]):\n    return x\n",
        )
        self.assertTrue(next(f for f in self._evaluate().findings if f.check == "AH013").blocking)

    def test_allow_for_a_different_check_does_not_suppress(self) -> None:
        self.write("s.py", "def f(x=[]):  # harness:allow AH999 - wrong id\n    return x\n")
        self.assertTrue(next(f for f in self._evaluate().findings if f.check == "AH013").blocking)

    def test_waiver_suppresses_within_its_path_scope(self) -> None:
        self.write("vendor/thing.py", "def f(x=[]):\n    return x\n")
        self.write("ours/thing.py", "def f(x=[]):\n    return x\n")
        waivers = Waivers(
            [Waiver(check="AH013", path="vendor/**", reason="third-party code", expires="2030-01-01")]
        )
        result = self._evaluate(waivers=waivers)
        by_path = {f.path: f.blocking for f in result.findings if f.check == "AH013"}
        self.assertFalse(by_path["vendor/thing.py"])
        self.assertTrue(by_path["ours/thing.py"])

    def test_expired_waiver_stops_suppressing_and_is_reported(self) -> None:
        self.write("vendor/thing.py", "def f(x=[]):\n    return x\n")
        waivers = Waivers(
            [Waiver(check="AH013", path="vendor/**", reason="temporary", expires="2020-01-01")]
        )
        result = self._evaluate(waivers=waivers)
        self.assertTrue(next(f for f in result.findings if f.check == "AH013").blocking)
        self.assertTrue(any("expired" in note for note in result.notes), result.notes)

    def test_waiver_without_a_reason_is_a_config_error(self) -> None:
        self.ws.waivers_path.write_text(
            json.dumps({"waivers": [{"check": "AH013", "path": "**"}]}), encoding="utf-8"
        )
        with self.assertRaises(ConfigError):
            Waivers.load(self.ws.waivers_path)


class TestPack(TempRepo):
    def test_build_refuses_an_unresolvable_slug(self) -> None:
        # The anti-fiction guard: delete one instruction and the pack must not compile.
        corpus = Corpus(self.corpus)
        victim = next(iter(CHECKS.values()))
        (self.corpus / f"{victim.slug}.md").unlink()
        with self.assertRaises(CorpusError) as caught:
            build_pack(Corpus(self.corpus), name="broken")
        self.assertIn(victim.slug, str(caught.exception))
        del corpus

    def test_near_miss_slug_gets_a_suggestion(self) -> None:
        corpus = Corpus(self.corpus)
        real = next(iter(CHECKS.values())).slug
        with self.assertRaises(CorpusError) as caught:
            corpus.get(real[:-1])
        self.assertIn("did you mean", str(caught.exception.hint or ""))

    def test_pack_digest_is_stable_and_excludes_created(self) -> None:
        first = build_pack(Corpus(self.corpus), name="p", limit=0)
        second = build_pack(Corpus(self.corpus), name="p", limit=0)
        self.assertEqual(first.digest, second.digest)
        second.created = "2099-01-01T00:00:00Z"
        self.assertEqual(first.digest, second.digest)

    def test_pack_name_changes_the_digest(self) -> None:
        self.assertNotEqual(
            build_pack(Corpus(self.corpus), name="a", limit=0).digest,
            build_pack(Corpus(self.corpus), name="b", limit=0).digest,
        )

    def test_edited_pack_file_is_refused_on_load(self) -> None:
        pack = build_pack(Corpus(self.corpus), name="edited", limit=0)
        path = save_pack(self.ws.policy_dir, pack)
        payload = json.loads(path.read_text(encoding="utf-8"))
        # Flip it to a value it demonstrably is not, so the edit cannot be a no-op if
        # rule ordering changes later.
        target = payload["rules"][0]
        target["severity"] = "info" if target["severity"] != "info" else "error"
        path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(IntegrityError):
            load_pack(self.ws.policy_dir, "edited")

    def test_drift_is_detected_when_an_instruction_changes(self) -> None:
        pack = build_pack(Corpus(self.corpus), name="drifty", limit=0)
        victim = pack.rules[0]
        path = self.corpus / f"{victim.slug}.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nAn added sentence.\n", encoding="utf-8")
        drift = pack.drift(Corpus(self.corpus))
        self.assertEqual([d["slug"] for d in drift], [victim.slug])
        self.assertEqual(drift[0]["state"], "changed")

    def test_drift_is_detected_when_an_instruction_is_removed(self) -> None:
        pack = build_pack(Corpus(self.corpus), name="gone", limit=0)
        (self.corpus / f"{pack.rules[0].slug}.md").unlink()
        self.assertEqual(pack.drift(Corpus(self.corpus))[0]["state"], "removed")

    def test_pack_severity_overrides_the_check_default(self) -> None:
        pack = build_pack(Corpus(self.corpus), name="p", limit=0)
        from dataclasses import replace

        pack.rules = [replace(r, severity="info") if r.id == "AH001" else r for r in pack.rules]
        self.assertEqual(pack.checks()["AH001"].severity, "info")

    def test_unknown_check_id_is_a_usage_error(self) -> None:
        with self.assertRaises(UsageError):
            build_pack(Corpus(self.corpus), name="p", check_ids=["AH999"])

    def test_advisory_rules_do_not_duplicate_machine_rules(self) -> None:
        pack = build_pack(Corpus(self.corpus), name="p", topics=["Security"], limit=50)
        machine = {r.slug for r in pack.machine_rules}
        advisory = {r.slug for r in pack.advisory_rules}
        self.assertEqual(machine & advisory, set())

    def test_threshold_must_be_a_known_severity(self) -> None:
        with self.assertRaises(UsageError):
            build_pack(Corpus(self.corpus), name="p", threshold="critical")


class TestAdvisoryBundle(TempRepo):
    def test_bundle_matches_by_language_selector(self) -> None:
        pack = build_pack(Corpus(self.corpus), name="p", topics=["Security"], limit=50)
        bundle, slugs, _ = advisory_bundle(pack, Corpus(self.corpus), ["app.py"])
        self.assertTrue(slugs)
        self.assertIn("Review context", bundle)
        for slug in slugs:
            self.assertIn(slug, bundle)

    def test_nothing_matches_an_unrelated_file_type(self) -> None:
        pack = build_pack(Corpus(self.corpus), name="p", languages=["Python"], limit=50)
        pack.rules = [r for r in pack.rules if r.enforcement == "advisory" and r.selector != ("**",)]
        _, slugs, _ = advisory_bundle(pack, Corpus(self.corpus), ["styles.css"])
        self.assertEqual(slugs, [])

    def test_a_pack_with_no_facet_filter_pins_the_whole_corpus(self) -> None:
        # The pack's digest has to mean "this policy", not "the most-discussed slice of
        # it as of whenever this was built".
        corpus = Corpus(self.corpus)
        pack = build_pack(corpus, name="everything")
        self.assertEqual(len(pack.rules), len(corpus), f"{len(pack.rules)} rules for {len(corpus)} instructions")

    def test_topics_are_detected_from_the_change_itself(self) -> None:
        from awesome_harness.policy.engine import change_topics

        concurrency = change_topics(
            ["svc.py"], {"svc.py": [(1, "async def run():"), (2, "    async with Lock():")]}
        )
        self.assertIn("Concurrency", concurrency)
        self.assertNotIn("Database", concurrency)

        database = change_topics(["repo.py"], {"repo.py": [(1, "stmt = select(User).where(User.id == key)")]})
        self.assertIn("Database", database)

    def test_on_topic_instructions_outrank_off_topic_ones(self) -> None:
        # The whole point of ranking: a pack holding thousands of rules must not hand a
        # concurrency change a pile of unrelated advice just because it is popular.
        corpus = Corpus(self.corpus)
        pack = build_pack(corpus, name="ranked")
        added = {"svc.py": [(1, "async def run():"), (2, "    async with Lock():")]}
        _, slugs, _ = advisory_bundle(pack, corpus, ["svc.py"], added=added, max_rules=1)
        self.assertEqual(slugs, ["fixture-coordinate-concurrent-access"])

    def test_a_different_change_gets_different_instructions(self) -> None:
        corpus = Corpus(self.corpus)
        pack = build_pack(corpus, name="ranked")
        _, concurrency, _ = advisory_bundle(
            pack, corpus, ["svc.py"],
            added={"svc.py": [(1, "async with Lock():")]}, max_rules=1,
        )
        _, database, _ = advisory_bundle(
            pack, corpus, ["repo.py"],
            added={"repo.py": [(1, "stmt = select(User).where(User.id == key)")]}, max_rules=1,
        )
        self.assertNotEqual(concurrency, database, "ranking must respond to the change")
        self.assertEqual(database, ["fixture-query-through-a-session"])

    def test_the_ranking_note_names_the_detected_topics(self) -> None:
        corpus = Corpus(self.corpus)
        pack = build_pack(corpus, name="ranked")
        _, _, notes = advisory_bundle(
            pack, corpus, ["a.py"], added={"a.py": [(1, "try:"), (2, "except ValueError:")]}
        )
        self.assertTrue(any("Error Handling" in note for note in notes), notes)

    def test_a_capped_bundle_says_what_it_dropped(self) -> None:
        pack = build_pack(Corpus(self.corpus), name="p", topics=["Security"], limit=50)
        _, slugs, notes = advisory_bundle(pack, Corpus(self.corpus), ["app.py"], max_rules=1)
        self.assertEqual(len(slugs), 1)
        self.assertTrue(any("omitted" in note for note in notes), notes)


class TestSelectors(unittest.TestCase):
    def test_star_does_not_cross_a_separator(self) -> None:
        self.assertTrue(matches_selector("a.py", ("*.py",)))
        self.assertFalse(matches_selector("pkg/a.py", ("*.py",)))

    def test_double_star_is_recursive_and_matches_the_root(self) -> None:
        self.assertTrue(matches_selector("a.py", ("**/*.py",)))
        self.assertTrue(matches_selector("deep/nested/a.py", ("**/*.py",)))

    def test_braces_expand(self) -> None:
        self.assertTrue(matches_selector("x.yaml", ("**/*.{yml,yaml}",)))
        self.assertFalse(matches_selector("x.json", ("**/*.{yml,yaml}",)))

    def test_bare_double_star_matches_everything(self) -> None:
        for path in ("a", "a/b/c.txt", ".github/workflows/x.yml"):
            self.assertTrue(matches_selector(path, ("**",)), path)


@unittest.skipUnless(REAL_CORPUS.is_dir(), "the awesome-reviewers corpus is not vendored here")
class TestRealCorpus(unittest.TestCase):
    """The citations must be real. This is the test that keeps them honest."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = Corpus(REAL_CORPUS)

    def test_every_check_slug_resolves_to_a_real_instruction(self) -> None:
        for check in CHECKS.values():
            with self.subTest(check=check.id):
                instruction = self.corpus.get(check.slug)
                self.assertTrue(instruction.body.strip(), check.slug)
                self.assertTrue(instruction.repository, f"{check.slug} has no source repository")

    def test_checks_draw_on_more_than_one_repository(self) -> None:
        repositories = {self.corpus.get(c.slug).repository for c in CHECKS.values()}
        self.assertGreater(len(repositories), 8, f"only {len(repositories)} source repositories: {repositories}")

    def test_corpus_parses_at_scale(self) -> None:
        self.assertGreater(len(self.corpus), 1000)
        sample = next(iter(self.corpus))
        self.assertTrue(sample.title and sample.body and sample.digest)


if __name__ == "__main__":
    unittest.main()
