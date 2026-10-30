---
title: Scope secret-scanning allowlists narrowly
description: When adding exemptions to secret-scanning tools (e.g., gitleaks), scope
  allowlist rules as narrowly as possible so they exclude only the specific known-safe
  values (such as synthetic/test model IDs) without weakening detection of real secrets
  elsewhere. Use precise rule targeting—e.g., restrict to a specific rule ID, combine
  conditions with AND, and set...
repository: cline/cline#"><b>zze3729958
label: Security
language: Toml
comments_count: 1
repository_stars: 71067
---

When adding exemptions to secret-scanning tools (e.g., gitleaks), scope allowlist rules as narrowly as possible so they exclude only the specific known-safe values (such as synthetic/test model IDs) without weakening detection of real secrets elsewhere. Use precise rule targeting—e.g., restrict to a specific rule ID, combine conditions with AND, and set regexTarget to match the exact value—rather than broad path- or file-level exemptions. After adding an exemption, verify it works as intended: confirm the specific allowed values are ignored, and confirm that an unrelated secret-like string in the same file/path is still flagged. Example from a fix:

```toml
[[allowlists]]
  description = "Allow known synthetic model IDs"
  targetRules = ["generic-api-key"]
  condition = "AND"
  regexTarget = "match"
  regexes = [
    '''synthetic-model-id-1''',
    '''synthetic-model-id-2''',
    # ...
  ]
```

This ensures secret-scanning exemptions remain tight and auditable, preventing accidental suppression of genuine credential leaks.