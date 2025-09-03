---
title: optimize CI performance
description: Structure CI workflows to minimize execution time and resource usage
  through strategic job organization, caching, and elimination of redundant operations.
repository: browser-use/browser-use
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 69139
---

Structure CI workflows to minimize execution time and resource usage through strategic job organization, caching, and elimination of redundant operations.

Key optimization strategies:
- **Split jobs for parallelization**: Break monolithic jobs into separate parallel jobs that can run concurrently, especially for linting, formatting, and type checking
- **Use cached actions**: Prefer off-the-shelf actions with built-in caching over manual installations that repeat on every run
- **Eliminate redundant steps**: Remove duplicate installations or commands that are already handled elsewhere in the workflow
- **Separate build from test matrix**: Build artifacts once without matrix, then test across multiple environments using the cached artifacts

Example of optimized job structure:
```yaml
jobs:
  # Fast parallel checks (each ~20sec)
  syntax-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv run ruff check --no-fix --select PLE
  
  format-check:
    runs-on: ubuntu-latest  
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv run ruff format
      - run: uv run pre-commit run --all-files
      
  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6  
      - run: uv run pyright

  # Build once, test across matrix
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          
  test-import:
    needs: build
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.11", "3.12", "3.13"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - run: python -c "import browser_use; print('Success!')"
```

This approach reduces total CI time from sequential execution to parallel execution, with all checks completing in under 30 seconds instead of several minutes.