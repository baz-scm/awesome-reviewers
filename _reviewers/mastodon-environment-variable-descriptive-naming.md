---
title: Environment variable descriptive naming
description: Environment variables should use descriptive, specific names that clearly
  indicate their purpose and scope to avoid conflicts and improve maintainability.
  Generic names can lead to confusion when multiple features need similar configuration
  options.
repository: mastodon/mastodon
label: Configurations
language: Other
comments_count: 2
repository_stars: 48691
---

Environment variables should use descriptive, specific names that clearly indicate their purpose and scope to avoid conflicts and improve maintainability. Generic names can lead to confusion when multiple features need similar configuration options.

Use specific, self-documenting names that include the feature or component they control:

```bash
# Avoid generic names
MFA_FORCE=true
MAX_CHARS=500

# Use descriptive, specific names
REQUIRE_MULTI_FACTOR_AUTH=true
MAX_TOOT_CHARS=500
```

This practice prevents naming conflicts when different features need similar configuration (e.g., character limits for posts vs. bios) and makes the configuration's intent immediately clear to developers. Additionally, avoid leaving test-specific environment variables in development configuration files to prevent confusion about which settings are actually required for the application to function.