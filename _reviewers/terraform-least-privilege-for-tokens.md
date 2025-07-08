---
title: Least privilege for tokens
description: 'Always apply the principle of least privilege when configuring access
  tokens for CI/CD workflows and other automated processes. Use fine-grained tokens
  or permissions that grant only the minimum necessary access required for the specific
  operations. '
repository: hashicorp/terraform
label: Security
language: Yaml
comments_count: 1
repository_stars: 45532
---

Always apply the principle of least privilege when configuring access tokens for CI/CD workflows and other automated processes. Use fine-grained tokens or permissions that grant only the minimum necessary access required for the specific operations. 

For example, if a GitHub workflow only needs to trigger actions in a specific repository, limit the token's scope to just that repository and only the "Actions (Read and write)" permission:

```yaml
# Example GitHub workflow using fine-grained token
- name: Setup workflow
  uses: hashicorp/action-setup-bob@v1
  with:
    github-token: ${{ secrets.LIMITED_SCOPE_TOKEN }}
    # Token configured with:
    # - Access to only this specific repository
    # - Only Actions (Read and write) permission
    # - No other permissions granted
```

This reduces the security risk if tokens are ever compromised by limiting the potential impact of a security breach. When using service accounts or tokens in any context, document the exact permissions granted and regularly audit them to ensure they remain appropriate.