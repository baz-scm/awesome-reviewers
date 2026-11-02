---
title: Minimal, portable configuration
description: 'Keep shared configuration files lean, portable, and explicit so they
  work correctly for every contributor and environment. Specifically:


  - Do not commit IDE- or machine-specific artifacts (e.g. `.idea/*.iml`) into the
  repository. Add them to `.git/info/exclude` or a local `.gitignore` instead of checking
  them in.'
repository: pallets/flask#x
label: Configurations
language: Other
comments_count: 4
repository_stars: 75163
---

Keep shared configuration files lean, portable, and explicit so they work correctly for every contributor and environment. Specifically:

- Do not commit IDE- or machine-specific artifacts (e.g. `.idea/*.iml`) into the repository. Add them to `.git/info/exclude` or a local `.gitignore` instead of checking them in.
- Keep the default/shared config (e.g. `setup.cfg`) minimal so common commands work out of the box without forcing extra installs. Put optional or environment-specific overrides (e.g. running tests against `examples`) in the tool that manages variants, such as `tox.ini` with `testpaths = {posargs:tests examples}`, rather than hardcoding them in the base config.
- Avoid configuration options tied to a specific legacy tool or VCS (e.g. `tag_svn_revision`) when a more general, portable option exists (e.g. `tag_build`/`tag_date`).
- Make supported environments explicit rather than implicit: declare supported Python versions via `python_requires` in `setup.py`, and keep this in sync with documented/tested version support.

Applying these guidelines keeps configuration files predictable, avoids breaking default workflows for other developers, and makes supported environments and dependencies explicit and verifiable.