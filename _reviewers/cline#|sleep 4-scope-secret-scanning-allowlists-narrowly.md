---
title: Scope secret-scanning allowlists narrowly
description: When adding exemptions to secret-scanning tools (e.g., gitleaks allowlists)
  for known false positives such as synthetic test IDs or fixtures, scope the exemption
  as narrowly as possible so it cannot mask real credentials. Use precise rule targeting,
  combined conditions (e.g., condition = AND), and exact match regexes (regexTarget
  = match) rather than broad...
repository: cline/cline#|sleep 4
label: Security
language: Toml
comments_count: 1
repository_stars: 70979
---

When adding exemptions to secret-scanning tools (e.g., gitleaks allowlists) for known false positives such as synthetic test IDs or fixtures, scope the exemption as narrowly as possible so it cannot mask real credentials. Use precise rule targeting, combined conditions (e.g., condition = AND), and exact match regexes (regexTarget = match) rather than broad path- or pattern-based exclusions. After adding an allowlist entry, verify both that the intended false positives are suppressed and that an unrelated real-looking secret in the same file/path is still flagged. Example:

```toml
[[allowlists]]
description = "Synthetic model IDs used in tests"
targetRules = ["generic-api-key"]
condition = "AND"
regexTarget = "match"
regexes = [
  '''sk-test-model-id-1''',
  '''sk-test-model-id-2''',
  # ... only the exact known synthetic values
]
paths = ['''tests/fixtures/models\.json''']
```

This ensures secret-scanning exemptions don't become loopholes that let real leaked secrets slip through undetected.</description>
</invoke>
