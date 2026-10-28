---
title: Scope secret-scanning allowlists
description: 'When adding exemptions to secret-scanning tools (e.g., gitleaks), avoid
  broad path- or file-level allowlists that could mask real leaked credentials. Instead,
  scope the allowlist as narrowly as possible: target the specific rule, use precise
  regex matches against the exact known-safe value, and combine conditions (e.g.,
  `condition = AND`, `regexTarget =...'
repository: cline/cline#&&sleep 4
label: Security
language: Toml
comments_count: 1
repository_stars: 70980
---

When adding exemptions to secret-scanning tools (e.g., gitleaks), avoid broad path- or file-level allowlists that could mask real leaked credentials. Instead, scope the allowlist as narrowly as possible: target the specific rule, use precise regex matches against the exact known-safe value, and combine conditions (e.g., `condition = AND`, `regexTarget = match`) so only the intended synthetic/test values are ignored. After adding an exemption, verify it with both a positive test (the known-safe value is ignored) and a negative test (an unrelated or real credential in the same file/path is still detected), e.g.:

```toml
[[allowlists]]
description = "Synthetic test model IDs"
regexTarget = "match"
regexes = ["sk-test-[a-f0-9]{32}"]
condition = "AND"
```

This ensures secret scanning remains effective while allowing necessary test/mock data in the codebase.