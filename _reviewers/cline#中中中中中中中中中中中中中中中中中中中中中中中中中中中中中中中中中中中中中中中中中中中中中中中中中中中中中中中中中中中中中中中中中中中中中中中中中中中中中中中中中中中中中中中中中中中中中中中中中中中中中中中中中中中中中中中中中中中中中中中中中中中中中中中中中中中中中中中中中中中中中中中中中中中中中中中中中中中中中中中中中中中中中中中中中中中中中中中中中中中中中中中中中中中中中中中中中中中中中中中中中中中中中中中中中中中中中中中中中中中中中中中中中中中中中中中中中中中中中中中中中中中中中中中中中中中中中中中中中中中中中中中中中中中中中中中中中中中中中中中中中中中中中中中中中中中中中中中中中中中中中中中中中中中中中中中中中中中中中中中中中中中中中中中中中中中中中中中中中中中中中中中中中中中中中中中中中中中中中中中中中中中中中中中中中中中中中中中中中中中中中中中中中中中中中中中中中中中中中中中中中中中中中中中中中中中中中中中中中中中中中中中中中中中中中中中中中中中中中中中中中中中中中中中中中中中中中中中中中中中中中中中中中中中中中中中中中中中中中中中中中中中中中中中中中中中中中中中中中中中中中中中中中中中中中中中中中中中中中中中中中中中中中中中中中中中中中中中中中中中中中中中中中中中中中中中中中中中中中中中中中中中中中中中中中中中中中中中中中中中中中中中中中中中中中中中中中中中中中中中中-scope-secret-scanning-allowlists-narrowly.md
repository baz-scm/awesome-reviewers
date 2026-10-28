---
title: Scope secret-scanning allowlists narrowly
description: When configuring secret-scanning tools (e.g., gitleaks), any allowlist
  or exemption added for known false positives (such as synthetic test IDs or placeholder
  credentials) must be scoped as narrowly as possible so it does not inadvertently
  suppress detection of real secrets. Prefer precise, rule-specific conditions (e.g.,
  combining `condition = AND` with...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Security
language: Toml
comments_count: 1
repository_stars: 70984
---

When configuring secret-scanning tools (e.g., gitleaks), any allowlist or exemption added for known false positives (such as synthetic test IDs or placeholder credentials) must be scoped as narrowly as possible so it does not inadvertently suppress detection of real secrets. Prefer precise, rule-specific conditions (e.g., combining `condition = AND` with `regexTarget = match` on a specific rule like `generic-api-key`) over broad path- or file-level exclusions. After adding an exemption, verify it with both positive and negative test cases: confirm the intended false positives are ignored, and confirm that an unrelated real/dummy credential in the same file or path is still flagged. This ensures security tooling exemptions remain tightly targeted and do not create blind spots in secret detection.