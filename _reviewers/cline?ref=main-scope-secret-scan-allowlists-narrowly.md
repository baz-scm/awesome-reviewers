---
title: Scope secret-scan allowlists narrowly
description: When adding exemptions to secret-scanning configurations (e.g., .gitleaks.toml
  allowlists), scope them as narrowly as possible so only the specific known-safe
  values (such as synthetic/test model IDs) are excluded, rather than broadly matching
  patterns that could hide real credentials. Use precise match conditions (e.g., condition
  = AND combined with...
repository: cline/cline?ref=main
label: Security
language: Toml
comments_count: 1
repository_stars: 70980
---

When adding exemptions to secret-scanning configurations (e.g., .gitleaks.toml allowlists), scope them as narrowly as possible so only the specific known-safe values (such as synthetic/test model IDs) are excluded, rather than broadly matching patterns that could hide real credentials. Use precise match conditions (e.g., condition = AND combined with regexTarget = match) to tie the exemption to both the rule and the exact value. After adding an allowlist entry, verify it with a test: confirm the intended safe values are ignored while an unrelated real-looking secret at the same location or pattern is still flagged. This prevents overly permissive allowlists from creating blind spots in credential detection.</description>
</invoke>
