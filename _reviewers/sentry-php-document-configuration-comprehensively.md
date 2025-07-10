---
title: Document configuration comprehensively
description: When adding or modifying configuration options, ensure they are documented
  with complete context. Group related changes together (like deprecation and default
  value changes), include reference numbers, and explain the purpose and effect of
  configuration options. This helps users understand how to properly configure the
  system without confusion.
repository: getsentry/sentry-php
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 1873
---

When adding or modifying configuration options, ensure they are documented with complete context. Group related changes together (like deprecation and default value changes), include reference numbers, and explain the purpose and effect of configuration options. This helps users understand how to properly configure the system without confusion.

For example, instead of:
```
- Add `in_app_include` option
```

Use:
```
- Add `in_app_include` option to whitelist paths that should be marked as part of the app (#909)
```

Similarly, related configuration changes should be documented together:
```
- Lower the default `send_attempts` option to `0` (disabling retries) and deprecate this option in favor of the new retry mechanism (#1312)
```