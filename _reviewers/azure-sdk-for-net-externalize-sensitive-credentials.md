---
title: Externalize sensitive credentials
description: Never hardcode sensitive values such as client identifiers, API keys,
  connection strings, or passwords directly in code or configuration files. Instead,
  use secure mechanisms like environment variables, secret managers, or pipeline variable
  groups to inject these values at runtime. This practice reduces the risk of credential
  exposure in version control...
repository: Azure/azure-sdk-for-net
label: Security
language: Yaml
comments_count: 1
repository_stars: 5809
---

Never hardcode sensitive values such as client identifiers, API keys, connection strings, or passwords directly in code or configuration files. Instead, use secure mechanisms like environment variables, secret managers, or pipeline variable groups to inject these values at runtime. This practice reduces the risk of credential exposure in version control systems and unauthorized access if the repository is compromised.

Example:
```yaml
# Avoid this:
task: EsrpRelease@9
inputs:
  ClientId: '5f81938c-2544-4f1f-9251-dd9de5b8a81b'
  
# Do this instead:
task: EsrpRelease@9
inputs:
  ClientId: $(ClientId)
```
