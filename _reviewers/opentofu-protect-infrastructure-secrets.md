---
title: Protect infrastructure secrets
description: 'Infrastructure-as-code tools like OpenTofu may store sensitive information
  in plaintext state files, creating security risks for passwords, API keys, and other
  secrets. Always implement proper protection measures:'
repository: opentofu/opentofu
label: Security
language: Markdown
comments_count: 2
repository_stars: 25901
---

Infrastructure-as-code tools like OpenTofu may store sensitive information in plaintext state files, creating security risks for passwords, API keys, and other secrets. Always implement proper protection measures:

1. Use ephemeral resources or write-only attributes when available to prevent secrets from being persisted
2. Consider state encryption as an additional security layer for all sensitive data
3. For write-only attributes that need updates, implement proper versioning triggers

When implementing secrets management, be aware of the tradeoffs:
- Ephemeral resources don't store secrets at all (reducing risk of leaked credentials)
- State encryption protects all secrets but requires secure key management

Example configuration using write-only attributes:
```hcl
resource "example_resource" "secure_resource" {
  name = "my-secure-resource"
  
  # Write-only attribute for sensitive data
  password = var.sensitive_password
  
  # Version attribute to trigger updates when password changes
  password_version = var.password_version
}
```

Remember that sensitive data can appear in plan files, state files, and logs unless properly managed. Always audit your infrastructure code for potential secret exposure.