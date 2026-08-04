"""Test fixtures: a throwaway git repository and a synthetic instruction corpus.

The corpus fixture is generated from the check registry itself, so a check added
without a resolvable slug fails a test rather than shipping a rule that cites
nothing.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from awesome_harness.policy.checks import CHECKS
from awesome_harness.workspace import Workspace


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=60,
        env={
            **os.environ,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_AUTHOR_NAME": "Test Runner",
            "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "Test Runner",
            "GIT_COMMITTER_EMAIL": "test@example.invalid",
        },
    )
    if completed.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


INSTRUCTION_TEMPLATE = """---
title: {title}
description: Synthetic fixture instruction for {slug}.
repository: fixture/{repo}
label: {label}
language: {language}
comments_count: 3
repository_stars: 1000
---

{body}
"""


def write_corpus(directory: Path, *, extra: dict[str, str] | None = None) -> Path:
    """Write one instruction file per registered check, plus any extras.

    Every check's slug gets a file, so `build_pack` can resolve all of them. The
    bodies are synthetic; what is under test is the resolution and pinning, not the
    prose.
    """
    directory.mkdir(parents=True, exist_ok=True)
    languages = {"AH004": "Python", "AH002": "Yaml", "AH015": "Dockerfile"}
    for index, check in enumerate(CHECKS.values()):
        (directory / f"{check.slug}.md").write_text(
            INSTRUCTION_TEMPLATE.format(
                title=check.summary[:60],
                slug=check.slug,
                repo=check.slug.split("-")[0],
                label=["Security", "CI/CD", "Error Handling", "Configurations"][index % 4],
                language=languages.get(check.id, "Python"),
                body=f"Rule body for {check.slug}.\n\nDo the right thing, in the way the reviewers described.",
            ),
            encoding="utf-8",
        )
    # Advisory-only instructions: no check binds to these, so they are what the
    # advisory tier has to select from. Without them a pack built from this corpus
    # would have nothing advisory in it, because every check slug is deduplicated out.
    advisory = {
        "fixture-review-error-messages": ("Security", "Python"),
        "fixture-name-things-for-behaviour": ("Security", "Python"),
        "fixture-keep-functions-small": ("Security", "Python"),
        "fixture-test-the-boundaries": ("Error Handling", "Python"),
        "fixture-document-the-contract": ("Configurations", "Python"),
        "fixture-workflow-hygiene": ("CI/CD", "Yaml"),
        "fixture-config-in-one-place": ("Configurations", "Yaml"),
    }
    for slug, (label, language) in advisory.items():
        (directory / f"{slug}.md").write_text(
            INSTRUCTION_TEMPLATE.format(
                title=slug.replace("fixture-", "").replace("-", " ").title(),
                slug=slug,
                repo="advisory",
                label=label,
                language=language,
                body=f"Advisory guidance body for {slug}. Reviewers said this repeatedly.",
            ),
            encoding="utf-8",
        )

    for slug, body in (extra or {}).items():
        (directory / f"{slug}.md").write_text(
            INSTRUCTION_TEMPLATE.format(
                title=slug.replace("-", " ").title(),
                slug=slug,
                repo="extra",
                label="Security",
                language="Python",
                body=body,
            ),
            encoding="utf-8",
        )
    return directory


class TempRepo(unittest.TestCase):
    """A git repository with an initialized harness and a synthetic corpus."""

    def setUp(self) -> None:
        self._tmp = tempfile.mkdtemp(prefix="harness-test-")
        self.root = Path(self._tmp).resolve()
        git(self.root, "init", "--quiet", "--initial-branch=main")
        git(self.root, "config", "user.name", "Test Runner")
        git(self.root, "config", "user.email", "test@example.invalid")
        git(self.root, "config", "commit.gpgsign", "false")

        (self.root / "README.md").write_text("fixture repository\n", encoding="utf-8")
        git(self.root, "add", "-A")
        git(self.root, "commit", "--quiet", "-m", "initial")

        self.corpus = write_corpus(self.root / "corpus")
        self.ws = Workspace.open(self.root, require=False)
        self.ws.root = self.root
        self.ws.initialize(corpus="corpus")
        # Reopen so the persisted config (including the corpus path) is what is read.
        self.ws = Workspace.open(self.root)

    def tearDown(self) -> None:
        shutil.rmtree(self._tmp, ignore_errors=True)

    # ---- helpers --------------------------------------------------------- #

    def write(self, relative: str, content: str, *, executable: bool = False) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if executable:
            path.chmod(0o755)
        return path

    def commit(self, message: str = "change") -> str:
        git(self.root, "add", "-A")
        git(self.root, "commit", "--quiet", "-m", message)
        return git(self.root, "rev-parse", "HEAD")


REAL_CORPUS = Path(__file__).resolve().parents[2] / "_reviewers"
