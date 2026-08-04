"""Pillar 1a — source control facts, and immutable snapshots of dirty work.

Git already is the durable, immutable history. The harness does not reimplement
it; it makes two things possible that git alone does not.

**Snapshots.** An agent's work exists as a dirty worktree long before it exists as
a commit, and that is exactly the window where you most want a durable record.
`snapshot()` writes the current worktree into real git objects through a temporary
index — `write-tree` then `commit-tree` — and anchors the result under
`refs/harness/snapshots/<run-id>`. Nothing is staged, no branch moves, no commit
is created on any branch, and yet the state becomes a content-addressed object
that git will not garbage-collect and that every other pillar can point at. The
tree oid is the content identity used in cache keys and attestation subjects; the
commit oid is the anchor a human can `git show`.

**Change scoping.** A gate that scans whole files punishes you for code you did
not write. Every check runs against the added lines of a diff, so the unit of
policy is the change, which is also the unit a reviewer would look at.

Derived from the corpus:
  aidlc-workflows-secure-scope-and-input-validation — never interpolate into a
      shell; pass argv and let git parse it.
  aidlc-workflows-fail-loudly-degrade-safely — `GIT_TERMINAL_PROMPT=0` so a repo
      needing credentials fails instead of hanging forever on a prompt.
  aidlc-workflows-defensive-observable-error-handling — a git failure reports the
      subcommand and stderr, not just a return code.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .errors import ExecutionError, HarnessError

# 40 hex for sha1 repositories, 64 for sha256 ones.
OID_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")

SNAPSHOT_REF_PREFIX = "refs/harness/snapshots"


class GitError(ExecutionError):
    kind = "git"


@dataclass(frozen=True)
class Snapshot:
    """An immutable git object graph capturing a worktree at a moment."""

    tree: str
    commit: str
    ref: str
    parent: str | None
    dirty: bool
    # Files differing from the parent commit, so a caller can see what the snapshot
    # actually captured beyond HEAD.
    changed: tuple[str, ...] = ()


@dataclass(frozen=True)
class Hunk:
    path: str
    line: int
    text: str


class Git:
    """Thin, explicit wrapper. One place that spawns git, one place that fails."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    # ---- plumbing -------------------------------------------------------- #

    def run(
        self,
        *args: str,
        check: bool = True,
        env: dict[str, str] | None = None,
        timeout: float = 120.0,
    ) -> str:
        command = ["git", "--no-optional-locks", *args]
        child_env = dict(os.environ)
        # A git that can prompt is a git that can hang a CI job for its whole
        # timeout with no output. Refuse instead.
        child_env["GIT_TERMINAL_PROMPT"] = "0"
        child_env.setdefault("GIT_CONFIG_NOSYSTEM", "0")
        if env:
            child_env.update(env)
        try:
            completed = subprocess.run(  # noqa: S603 - argv list, never a shell string
                command,
                cwd=self.root,
                env=child_env,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=timeout,
            )
        except FileNotFoundError as exc:
            raise GitError("git is not installed or not on PATH") from exc
        except subprocess.TimeoutExpired as exc:
            raise GitError(f"git {args[0]} timed out after {timeout:g}s") from exc
        if check and completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or "").strip().splitlines()
            raise GitError(
                f"git {' '.join(args)} failed ({completed.returncode}): "
                f"{detail[0] if detail else 'no output'}"
            )
        return completed.stdout.strip()

    def lines(self, *args: str, **kwargs: object) -> list[str]:
        out = self.run(*args, **kwargs)  # type: ignore[arg-type]
        return [line for line in out.split("\n") if line]

    # ---- facts ----------------------------------------------------------- #

    def is_repo(self) -> bool:
        try:
            return self.run("rev-parse", "--is-inside-work-tree") == "true"
        except HarnessError:
            return False

    def head(self) -> str | None:
        """HEAD's commit oid, or None in a repository with no commits yet."""
        try:
            return self.run("rev-parse", "--verify", "HEAD")
        except HarnessError:
            return None

    def head_tree(self) -> str | None:
        head = self.head()
        return self.run("rev-parse", f"{head}^{{tree}}") if head else None

    def branch(self) -> str:
        try:
            return self.run("rev-parse", "--abbrev-ref", "HEAD")
        except HarnessError:
            return "HEAD"

    def is_dirty(self) -> bool:
        return bool(self.run("status", "--porcelain", "--untracked-files=normal"))

    def merge_base(self, base: str) -> str | None:
        head = self.head()
        if not head:
            return None
        try:
            return self.run("merge-base", base, head)
        except HarnessError:
            # An unknown or unfetched base is a legitimate state in a shallow CI
            # clone. The caller decides whether to fall back to HEAD.
            return None

    def facts(self, base: str | None = None) -> dict[str, object]:
        """Everything about the repository worth recording in a ledger entry."""
        head = self.head()
        data: dict[str, object] = {
            "head": head,
            "tree": self.head_tree(),
            "branch": self.branch(),
            "dirty": self.is_dirty(),
        }
        if base:
            data["base"] = base
            data["merge_base"] = self.merge_base(base)
        remote = self.run("remote", "get-url", "origin", check=False)
        if remote:
            # Remote URLs carry embedded tokens more often than anyone admits.
            from .scrub import scrub_text

            data["origin"] = scrub_text(remote)
        return data

    # ---- change scoping -------------------------------------------------- #

    def changed_files(self, base: str | None = None, *, include_untracked: bool = True) -> list[str]:
        """Repository-relative paths added, copied, modified or renamed.

        Deletions are excluded: there is no content left to check, and a policy
        that fires on a deleted file cannot be satisfied.
        """
        if base:
            ref = self.merge_base(base) or base
            paths = self.lines("diff", "--name-only", "--diff-filter=ACMRT", ref)
        else:
            paths = self.lines("diff", "--name-only", "--diff-filter=ACMRT", "HEAD") if self.head() else []
        if include_untracked:
            paths += self.lines("ls-files", "--others", "--exclude-standard")
        # Sorted and de-duplicated: this list feeds a cache key.
        return sorted(set(paths))

    def added_lines(self, base: str | None = None) -> list[Hunk]:
        """Added lines with their new-file line numbers.

        `-U0` so only additions come back, and untracked files are diffed against
        the empty tree so a brand-new file is fully in scope. Scanning additions
        rather than files is what keeps a gate from blaming a change for code that
        was already there.
        """
        args = ["diff", "--no-color", "--no-ext-diff", "-U0", "--diff-filter=ACMRT"]
        if base:
            args.append(self.merge_base(base) or base)
        elif self.head():
            args.append("HEAD")
        else:
            args.append(self.run("hash-object", "-t", "tree", "/dev/null"))
        hunks = _parse_unified_diff(self.run(*args, check=False))

        for path in self.lines("ls-files", "--others", "--exclude-standard"):
            text = self.run(
                "diff", "--no-color", "--no-index", "-U0", "--", "/dev/null", path, check=False
            )
            hunks.extend(_parse_unified_diff(text, force_path=path))
        return hunks

    # ---- snapshots ------------------------------------------------------- #

    def snapshot(
        self,
        run_id: str,
        *,
        message: str,
        author: str = "awesome-harness <harness@localhost>",
        tmp_dir: Path | None = None,
    ) -> Snapshot:
        """Freeze the worktree into git objects without touching the index or any branch.

        Reproducible in the part that matters: the same worktree content always
        yields the same tree oid, so two runs over unchanged code agree on content
        identity even though their commit oids differ by timestamp.
        """
        parent = self.head()
        index_dir = tmp_dir or (self.root / ".harness" / "tmp")
        index_dir.mkdir(parents=True, exist_ok=True)
        index_path = index_dir / f"index-{run_id}"
        env = {"GIT_INDEX_FILE": str(index_path)}
        try:
            if parent:
                self.run("read-tree", parent, env=env)
            else:
                self.run("read-tree", "--empty", env=env)
            # Honours .gitignore, so build output stays out. `.harness` is excluded
            # explicitly on top of that, and the reason matters: the ledger and the
            # attestations live there and are committed to git, so including them would
            # make the snapshot tree change every time a record is appended. A tree
            # digest that moves with the harness's own bookkeeping cannot serve as
            # content identity — it would break cache keys, and it would void an
            # approval the instant the approval itself was recorded.
            self.run("add", "--all", "--", ".", ":(exclude).harness", env=env)
            tree = self.run("write-tree", env=env)

            commit_args = ["commit-tree", tree, "-m", message]
            if parent:
                commit_args += ["-p", parent]
            name, email = _split_author(author)
            commit = self.run(
                *commit_args,
                env={
                    **env,
                    "GIT_AUTHOR_NAME": name,
                    "GIT_AUTHOR_EMAIL": email,
                    "GIT_COMMITTER_NAME": name,
                    "GIT_COMMITTER_EMAIL": email,
                },
            )
            ref = f"{SNAPSHOT_REF_PREFIX}/{run_id}"
            # A ref, not a dangling object: unreferenced commits are gc bait, and a
            # history that can be garbage-collected is not durable.
            self.run("update-ref", ref, commit)
            changed = (
                self.lines("diff-tree", "--name-only", "-r", "--no-commit-id", parent, tree)
                if parent
                else self.lines("ls-tree", "-r", "--name-only", tree)
            )
            return Snapshot(
                tree=tree,
                commit=commit,
                ref=ref,
                parent=parent,
                dirty=bool(changed),
                changed=tuple(sorted(changed)),
            )
        finally:
            index_path.unlink(missing_ok=True)

    def list_snapshots(self) -> list[tuple[str, str]]:
        out = self.lines("for-each-ref", "--format=%(refname:short) %(objectname)", SNAPSHOT_REF_PREFIX)
        return [tuple(line.split(" ", 1)) for line in out if " " in line]  # type: ignore[misc]

    # ---- worktrees ------------------------------------------------------- #

    def add_worktree(self, commit: str, dest: Path) -> None:
        """Detached checkout of one commit — the isolated compute for a step.

        `--detach` and `--no-checkout=false`: no branch is created, so a step can
        never move a ref, and the checkout is of an immutable object.
        """
        if not OID_RE.match(commit):
            commit = self.run("rev-parse", "--verify", commit)
        dest.parent.mkdir(parents=True, exist_ok=True)
        self.run("worktree", "add", "--detach", "--force", str(dest), commit, timeout=600.0)

    def remove_worktree(self, dest: Path) -> None:
        """Best effort: a failed removal must not mask the step's own failure."""
        self.run("worktree", "remove", "--force", str(dest), check=False, timeout=300.0)
        self.run("worktree", "prune", check=False)


def _split_author(author: str) -> tuple[str, str]:
    match = re.match(r"^\s*(.*?)\s*<([^>]*)>\s*$", author)
    if not match:
        return author.strip() or "awesome-harness", "harness@localhost"
    return match.group(1) or "awesome-harness", match.group(2) or "harness@localhost"


_DIFF_HEADER = re.compile(r"^\+\+\+ (?:b/)?(.*)$")
_HUNK_HEADER = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def _parse_unified_diff(text: str, *, force_path: str | None = None) -> list[Hunk]:
    """Pull `(path, line, text)` out of `git diff -U0` output.

    Written by hand rather than shelled out to a diff parser because the harness
    ships with no dependencies, and because -U0 output is small and regular: a
    `+++` line names the file, an `@@` line gives the starting new-file line, and
    each following `+` line increments from there.
    """
    hunks: list[Hunk] = []
    path = force_path
    line_no = 0
    for raw in text.split("\n"):
        header = _DIFF_HEADER.match(raw)
        if header:
            candidate = header.group(1)
            path = force_path or (None if candidate == "/dev/null" else candidate)
            continue
        hunk = _HUNK_HEADER.match(raw)
        if hunk:
            line_no = int(hunk.group(1))
            continue
        if raw.startswith("+") and not raw.startswith("+++") and path:
            hunks.append(Hunk(path=path, line=line_no, text=raw[1:]))
            line_no += 1
    return hunks
