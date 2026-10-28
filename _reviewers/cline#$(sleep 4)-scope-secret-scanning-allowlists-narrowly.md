---
title: Scope secret-scanning allowlists narrowly
description: When adding exemptions to secret-scanning or security linting tools (e.g.,
  gitleaks allowlists) for known false positives such as synthetic test IDs, scope
  the rule as tightly as possible—use exact match conditions (e.g., condition = AND
  with regexTarget = match) rather than broad pattern-based exclusions. Overly permissive
  allowlist entries can...
repository: cline/cline#$(sleep 4)
label: Security
language: Toml
comments_count: 1
repository_stars: 70978
---

When adding exemptions to secret-scanning or security linting tools (e.g., gitleaks allowlists) for known false positives such as synthetic test IDs, scope the rule as tightly as possible—use exact match conditions (e.g., condition = AND with regexTarget = match) rather than broad pattern-based exclusions. Overly permissive allowlist entries can inadvertently mask real secrets that happen to share a file, path, or pattern with the exempted value. After adding or modifying an exemption, verify both that the intended false positives are suppressed and that an unrelated real secret in the same context is still flagged, e.g.:

```toml
[[allowlists]]
targetRule = "generic-api-key"
condition = "AND"
regexes = ["exact-synthetic-model-id-1", "exact-synthetic-model-id-2"]
regexTarget = "match"
```

This ensures security tooling remains effective and exemptions don't silently widen the attack surface for leaked credentials.