---
title: Align CI dependency installs
description: Static-analysis and type-checking CI jobs (e.g., Pyre) must install the
  same dependency set as the code they analyze. If a job type-checks the test suite,
  its environment needs the dev/test dependencies (e.g., pytest) that those files
  import, not just the runtime requirements. When a workflow only installs from a
  production requirements file (e.g.,...
repository: kyegomez/swarms#pi240310
label: CI/CD
language: Python
comments_count: 3
repository_stars: 7337
---

Static-analysis and type-checking CI jobs (e.g., Pyre) must install the same dependency set as the code they analyze. If a job type-checks the test suite, its environment needs the dev/test dependencies (e.g., pytest) that those files import, not just the runtime requirements. When a workflow only installs from a production requirements file (e.g., `requirements.txt`) while scanning `tests/`, every test file's `import pytest` becomes an "Undefined import" false positive — and because the tool only reports changed lines, each new or touched test file in a PR picks up noise that isn't actually caused by that change.

Do not fix this by adding dev-only packages (like pytest) to the production requirements file — that ships test tooling into every runtime install. Instead, fix the workflow itself: either install the dev dependency group (from `pyproject.toml`) before running the analysis step, or configure the tool to ignore known test-only imports. When reviewing a PR that triggers such warnings, verify whether the failure is a pre-existing environment/config gap affecting the whole repo (as evidenced by the same warning appearing across dozens of existing files) versus an issue introduced by the diff, and resolve/track environment gaps as separate CI infrastructure fixes rather than blocking the PR.