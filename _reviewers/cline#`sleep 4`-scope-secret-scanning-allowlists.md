---
title: Scope secret-scanning allowlists
description: When adding exceptions to secret-scanning tools (e.g., gitleaks) for
  known non-sensitive values such as synthetic test IDs or fixture data, scope the
  allowlist rule as narrowly as possible so it cannot mask genuine leaked credentials.
  Target the specific rule and exact value rather than broad path- or wildcard-based
  exclusions, and combine conditions (e.g.,...
repository: cline/cline#`sleep 4`
label: Security
language: Toml
comments_count: 1
repository_stars: 70979
---

When adding exceptions to secret-scanning tools (e.g., gitleaks) for known non-sensitive values such as synthetic test IDs or fixture data, scope the allowlist rule as narrowly as possible so it cannot mask genuine leaked credentials. Target the specific rule and exact value rather than broad path- or wildcard-based exclusions, and combine conditions (e.g., `condition = "AND"`) with a precise `regexTarget = "match"` so only the exact intended string is exempted.

Example:
```toml
[[allowlists]]
description = "Exempt synthetic test model IDs"
targetRules = ["generic-api-key"]
condition = "AND"
regexTarget = "match"
regexes = [
  '''sk-test-model-id-1''',
  '''sk-test-model-id-2''',
]
paths = ['''fixtures/models\.json''']
```

After adding any allowlist entry, verify it with a negative test: confirm the intended false positives are suppressed while an unrelated dummy credential in the same file/path is still detected. This prevents overly permissive exemptions from silently disabling secret detection.</description>
</invoke>
