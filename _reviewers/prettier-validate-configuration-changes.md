---
title: validate configuration changes
description: Configuration files require careful validation to ensure they work as
  intended and don't introduce unintended side effects. This includes verifying ignore
  patterns don't create parent-child conflicts, understanding rule severity implications,
  and confirming dependency changes are expected.
repository: prettier/prettier
label: Configurations
language: Other
comments_count: 4
repository_stars: 50772
---

Configuration files require careful validation to ensure they work as intended and don't introduce unintended side effects. This includes verifying ignore patterns don't create parent-child conflicts, understanding rule severity implications, and confirming dependency changes are expected.

For ignore patterns, ensure re-inclusion rules don't conflict with parent directory exclusions:
```
# Bad: Can't re-include files in ignored parent directories
/tests/format/**/*.*
!/tests/format/**/format.test.js

# Good: Re-include parent directories first
/tests/format/**/*.*
!/tests/format/**/*.*/
!/tests/format/**/format.test.js
```

For rule configurations, understand the difference between "error" and "warn" severity levels and use appropriate tooling flags like `--max-warnings=0` to enforce standards consistently.

For dependency changes, use tools like `yarn why` to understand why specific versions exist and `yarn-deduplicate` to clean up duplicate dependencies before merging.

Always test configuration changes locally and verify they produce the expected behavior across different scenarios.