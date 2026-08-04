---
title: Avoid glob file mutation
description: When automation modifies local files, don’t use broad filename globs
  that could match unexpected or attacker-controlled artifacts. Prefer deterministic,
  explicit paths/filenames (or fail closed). If a glob is unavoidable, validate that
  the matched file is exactly the expected artifact (e.g., match a known versioned
  filename pattern) before changing it.
repository: Azure/azure-cli
label: Security
language: Other
comments_count: 1
repository_stars: 4592
---

When automation modifies local files, don’t use broad filename globs that could match unexpected or attacker-controlled artifacts. Prefer deterministic, explicit paths/filenames (or fail closed). If a glob is unavoidable, validate that the matched file is exactly the expected artifact (e.g., match a known versioned filename pattern) before changing it.

Example (safer approach vs `for %%f in (python*._pth)`):
```bat
REM Prefer editing the exact expected file (derive/version-pin as appropriate)
set PTH_FILE=python312._pth
if exist %PTH_FILE% (
  findstr /x "import site" %PTH_FILE% >nul || echo import site>> %PTH_FILE%
) else (
  echo Expected %PTH_FILE% not found. Aborting.
  exit /b 1
)
```

This reduces unnecessary attack surface by ensuring your build logic only mutates the specific downloaded Python configuration file, not any other `python*._pth` that might appear in the directory.