---
title: Document authentication precedence
description: When implementing systems that support multiple authentication methods,
  always clearly document which authentication method takes precedence when multiple
  options are provided. This prevents security misconfigurations and ensures predictable
  behavior.
repository: ClickHouse/ClickHouse
label: Security
language: Markdown
comments_count: 1
repository_stars: 42425
---

When implementing systems that support multiple authentication methods, always clearly document which authentication method takes precedence when multiple options are provided. This prevents security misconfigurations and ensures predictable behavior.

Failing to document authentication precedence can lead to:
- Developers making incorrect assumptions about which credentials will be used
- Potential security vulnerabilities if weaker authentication methods are unexpectedly prioritized
- Inconsistent behavior across different environments

Example from Azure Blob Storage documentation:
```
- `account_key` - if storage_account_url is used, then account key can be specified here
- `extra_credentials` - Use `client_id` and `tenant_id` for authentication instead of `account_name` and `account_key`. If extra_credentials are provided, they are given priority over account name & account key.
```

Always explicitly state which authentication method will be used when multiple are configured, ensuring users understand the security implications of their configuration choices.