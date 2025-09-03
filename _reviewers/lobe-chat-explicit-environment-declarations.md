---
title: Explicit environment declarations
description: Always explicitly declare environment variables in configuration files,
  even when they have default values. Use consistent naming conventions with appropriate
  prefixes for related variables, and clearly document when each variable is required
  versus optional.
repository: lobehub/lobe-chat
label: Configurations
language: Other
comments_count: 4
repository_stars: 65138
---

Always explicitly declare environment variables in configuration files, even when they have default values. Use consistent naming conventions with appropriate prefixes for related variables, and clearly document when each variable is required versus optional.

This practice prevents configuration confusion and makes deployment requirements transparent. For example, instead of relying on implicit defaults, explicitly set values like `NEXT_PUBLIC_ENABLE_NEXT_AUTH=0` in environment files. Use consistent prefixes such as `AUTH_` for authentication-related variables, and provide clear documentation about when variables are needed (e.g., "necessary for self-hosting with Docker" vs "optional for most users").

```bash
# Good: Explicit declaration with clear naming
NEXT_PUBLIC_ENABLE_NEXT_AUTH=0
AUTH_GITHUB_CLIENT_ID=your_client_id
AUTH_GITHUB_CLIENT_SECRET=your_secret

# Bad: Missing explicit declaration, inconsistent naming
# NEXT_PUBLIC_ENABLE_NEXT_AUTH (relies on default)
GITHUB_CLIENT_ID=your_client_id  # Missing AUTH_ prefix
```

Document each variable's purpose and requirements in configuration guides, using callouts or tables to indicate when specific variables are mandatory for different deployment scenarios.