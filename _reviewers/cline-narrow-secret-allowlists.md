---
title: Narrow secret allowlists
description: When suppressing secret-scan findings (e.g., via gitleaks allowlists),
  keep exemptions narrowly scoped and verify the suppression boundaries. Use specific
  rule types and matching criteria (e.g., condition + regexTarget) rather than broad
  path-based ignores, and confirm that only the intended false positives are ignored
  while unrelated credentials at the...
repository: CLINE/CLINE
label: Security
language: Toml
comments_count: 1
repository_stars: 70837
---

When suppressing secret-scan findings (e.g., via gitleaks allowlists), keep exemptions narrowly scoped and verify the suppression boundaries. Use specific rule types and matching criteria (e.g., condition + regexTarget) rather than broad path-based ignores, and confirm that only the intended false positives are ignored while unrelated credentials at the same location are still detected.

Example (gitleaks-style allowlist):
```toml
[extend]
useDefault = true

[[allowlists]]
# Suppress only the intended generic API-key false positives
# with an explicit match target and strict condition.
# (Tune regexTarget/condition to your false-positive pattern.)
title = "Cline SDK secret scanning"

# Example shape:
# - condition: ensure both criteria must match
# - regexTarget: ensure matching is anchored to the expected field/value form
# (Keep this narrowly defined.)

# condition = "AND"
# regexTarget = "match"
# model = "<only intended synthetic IDs>"  # or equivalent precise selector
```

Verification checklist:
- Add/keep a test case for each intended synthetic model ID and ensure findings no longer trigger.
- Add a control test case with an unrelated dummy credential at the same path and ensure it still triggers a finding.
- Re-run the scan after configuration changes to confirm the allowlist has not widened.