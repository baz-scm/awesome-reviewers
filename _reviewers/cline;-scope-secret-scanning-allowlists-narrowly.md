---
title: Scope secret-scanning allowlists narrowly
description: When configuring secret-scanning tools (e.g., gitleaks), do not broadly
  allowlist patterns just to silence false positives. Instead, scope exemptions as
  tightly as possible using precise conditions (e.g., `condition = AND`, `regexTarget
  = match`, specific file paths or exact value matches) so that only the known false
  positives (such as synthetic/test model...
repository: cline/cline;
label: Security
language: Toml
comments_count: 1
repository_stars: 70964
---

When configuring secret-scanning tools (e.g., gitleaks), do not broadly allowlist patterns just to silence false positives. Instead, scope exemptions as tightly as possible using precise conditions (e.g., `condition = AND`, `regexTarget = match`, specific file paths or exact value matches) so that only the known false positives (such as synthetic/test model IDs) are excluded, while real secrets at the same location or matching a similar pattern are still flagged. After adding or modifying an allowlist rule, verify both outcomes: that the intended non-secret values are ignored, and that a known/representative real secret in the same context is still detected. This keeps the secret-scanning safety net effective while reducing noise.

Example:
```toml
[[allowlists]]
  description = "Synthetic model IDs are not real secrets"
  condition = "AND"
  regexTarget = "match"
  regexes = [
    '''sk-synthetic-model-[a-f0-9]{32}''',
  ]
  paths = [
    '''src/fixtures/models\.json''',
  ]
```
Always add a test case confirming an unrelated dummy credential at the same path is still caught.