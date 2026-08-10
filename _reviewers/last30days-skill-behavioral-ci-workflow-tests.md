---
title: Behavioral CI workflow tests
description: 'CI/CD workflow and release-automation checks must be deterministic and
  behavior-based.


  - Never “soft-skip” critical validations due to missing dev tooling; declare the
  needed test dependency (e.g., YAML parser) so the check always runs in CI.'
repository: mvanhorn/last30days-skill
label: CI/CD
language: Python
comments_count: 3
repository_stars: 57799
---

CI/CD workflow and release-automation checks must be deterministic and behavior-based.

- Never “soft-skip” critical validations due to missing dev tooling; declare the needed test dependency (e.g., YAML parser) so the check always runs in CI.
- Validate the real workflow logic (the same expressions/commands the workflow uses), not just that certain text fragments exist in the YAML.
- For release scripts invoked by CI, fail fast on invalid/unsafe inputs: validate semver, refuse downgrades, and clearly scope any exceptions to dry-run.

Example pattern (YAML parsing test):

```python
from pathlib import Path

path = Path('.github/workflows/tag-release.yml')
text = path.read_text(encoding='utf-8')

import yaml  # ensure pyyaml is in dev deps

yaml.safe_load(text)  # must run in CI; no ImportError bypass
```

Example pattern (behavioral parity): extract the exact command/expression from the workflow and run it against the representative inputs (e.g., direct vs merge-commit message shapes) rather than asserting only that the snippet appears in the file.

Finally, in release scripts:
- parse/validate versions
- block downgrades
- allow equality only when `--dry-run` is set.