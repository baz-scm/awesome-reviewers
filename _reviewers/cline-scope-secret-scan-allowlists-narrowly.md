---
title: Scope secret-scan allowlists narrowly
description: When adding exemptions to secret-scanning tools (e.g., gitleaks), avoid
  broad allowlist patterns that could mask real credentials. Tie each exemption to
  a specific rule ID and combine match conditions (e.g., condition = AND, regexTarget
  = match) so only the exact known-safe values (such as synthetic model IDs used in
  tests) are excluded. After adding an...
repository: cline/cline
label: Security
language: Toml
comments_count: 1
repository_stars: 70886
---

When adding exemptions to secret-scanning tools (e.g., gitleaks), avoid broad allowlist patterns that could mask real credentials. Tie each exemption to a specific rule ID and combine match conditions (e.g., condition = AND, regexTarget = match) so only the exact known-safe values (such as synthetic model IDs used in tests) are excluded. After adding an allowlist entry, verify that unrelated or real secrets placed in the same file/path are still flagged, confirming the exemption did not inadvertently widen detection gaps. Example: a generic-api-key allowlist rule should explicitly enumerate the safe values and require matching both the rule and exact string, not just the file path, to keep detection effective elsewhere in the same file.