---
title: CI workflow configuration best
description: 'Configure GitHub Actions workflows to maximize reliability and maintainability.
  Follow these key practices:


  1. **Always test with latest patches**: Use `check-latest: true` when setting up
  language environments to ensure you''re testing with the most recent patch versions
  rather than potentially outdated cached versions.'
repository: pola-rs/polars
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 34296
---

Configure GitHub Actions workflows to maximize reliability and maintainability. Follow these key practices:

1. **Always test with latest patches**: Use `check-latest: true` when setting up language environments to ensure you're testing with the most recent patch versions rather than potentially outdated cached versions.

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    check-latest: true
```

2. **Define complete job dependencies**: Ensure publication jobs depend on all build and test jobs to prevent publishing artifacts if any part of the build process fails.

```yaml
publish-to-pypi:
  needs: [create-sdist, build-wheels, build-wheel-pyodide]
```

3. **Use readable matrix configurations**: Consider using `include` rather than `exclude` when it results in clearer, more maintainable matrix definitions for cross-platform testing.

```yaml
matrix:
  package: [polars, polars-lts-cpu, polars-u64-idx]
  os: [ubuntu-latest, macos-13]
  architecture: [x86-64, aarch64]
  include:
    - os: windows-latest
      architecture: x86-64
    - os: windows-arm64-16gb
      architecture: aarch64
```

These practices help create reliable CI pipelines that catch issues early and prevent problematic releases.