---
title: Bounded, Consistent Extras
description: 'Whenever you change feature extras or dependency constraints in config
  (e.g., `pyproject.toml`), apply the same compatible version range everywhere that
  dependency is installed or resolved, and follow the dependency policy: bounded ranges
  only (no bare lower bounds; no conflicting exact pins). Regenerate the lockfile
  after the update.'
repository: nousresearch/hermes-agent
label: Configurations
language: Toml
comments_count: 3
repository_stars: 221948
---

Whenever you change feature extras or dependency constraints in config (e.g., `pyproject.toml`), apply the same compatible version range everywhere that dependency is installed or resolved, and follow the dependency policy: bounded ranges only (no bare lower bounds; no conflicting exact pins). Regenerate the lockfile after the update.

Checklist
- **Mirror constraints across install paths:** if an extra updates `numpy<2`, ensure the same constraint is used in any sibling/lazy dependency table or gateway installer logic.
- **Use bounded version ranges:** prefer policy-compliant ranges (e.g., for pre-1.0 `>=0.1.1,<0.3`), not exact pins like `==0.1.1`, and avoid declarations that only specify a lower bound (e.g., `pkg>=1.2` without an upper bound).
- **Refresh lockfiles:** after changing constraints, regenerate `uv.lock` so the resolved graph matches what CI/users install.
- **Keep config keys aligned with supported packages:** if a dependency removes/renames a feature, don’t leave dead configuration keys around.

Example (pattern)
```toml
# pyproject.toml
[project.optional-dependencies]
voice = [
  "numpy<2",
]

tenki = [
  "tenki>=0.5.1,<0.7",
]

native-fetch = [
  "readability-lxml>=0.8,<0.9",
  "html2text>=2024.0,<2025.0",
]
```
Then update any other install mechanism that still references the old pins/ranges, and run `uv lock` (or the repo’s standard lock regeneration step) so `uv.lock` reflects the same bounds.