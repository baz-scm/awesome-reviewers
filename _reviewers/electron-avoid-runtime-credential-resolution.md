---
title: avoid runtime credential resolution
description: Security credentials and access control mechanisms should be pre-configured
  at deployment or configuration time rather than resolved dynamically at runtime.
  Dynamic credential fetching introduces injection risks and makes security boundaries
  harder to audit and control.
repository: electron/electron
label: Security
language: Shell
comments_count: 2
repository_stars: 117644
---

Security credentials and access control mechanisms should be pre-configured at deployment or configuration time rather than resolved dynamically at runtime. Dynamic credential fetching introduces injection risks and makes security boundaries harder to audit and control.

Instead of fetching credentials from APIs or using runtime variables for security decisions, embed credentials in secure configuration stores (like Terraform-managed secrets) or integrate with centralized identity providers and zero-trust systems.

Example of problematic runtime resolution:
```bash
# Risky: Dynamic API call with potentially injectable variable
api_response=$(curl -s "https://api.github.com/users/$GITHUB_ACTOR/keys")
echo "$api_response" | jq -r '.[].key' > authorized_keys
```

Preferred approaches:
```bash
# Better: Pre-configured credentials from secure store
echo "$PRECONFIGURED_SSH_KEYS" > authorized_keys

# Best: Centralized identity-based access control
# Configure hostname as SSH target in zero-trust system
# Assign IDP roles (e.g., wg-infra) access to hostname
```

This approach eliminates injection vectors, improves auditability, and centralizes security policy management.