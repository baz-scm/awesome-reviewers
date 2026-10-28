---
title: Scope secret-scanning allowlists narrowly
description: When adding allowlist exemptions to secret-scanning tools (e.g., gitleaks),
  scope them as narrowly as possible so legitimate test/synthetic values are ignored
  without masking detection of real secrets. Prefer precise, combined conditions (e.g.,
  condition = AND with regexTarget = match) over broad path- or file-based exemptions,
  and match on the exact value...
repository: "cline/cline\r\n"
label: Security
language: Toml
comments_count: 1
repository_stars: 70946
---

When adding allowlist exemptions to secret-scanning tools (e.g., gitleaks), scope them as narrowly as possible so legitimate test/synthetic values are ignored without masking detection of real secrets. Prefer precise, combined conditions (e.g., condition = AND with regexTarget = match) over broad path- or file-based exemptions, and match on the exact value pattern rather than just the location. After adding or changing an allowlist rule, verify both that the intended synthetic values are suppressed and that an unrelated dummy credential placed in the same file/path is still flagged, to confirm the exemption has not created a blind spot for real secrets.

Example (gitleaks):
```toml
[[allowlists]]
description = "Allow known synthetic model IDs"
targetRules = ["generic-api-key"]
regexTarget = "match"
regexes = [
  '''sk-synthetic-[a-f0-9]{32}''', # only matches the specific test IDs, not any key in the file
]
condition = "AND"
```