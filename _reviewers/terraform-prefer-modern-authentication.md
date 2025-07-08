---
title: Prefer modern authentication
description: Always use modern identity-based authentication methods instead of static
  credentials when accessing external systems. This reduces security risks associated
  with credential management, rotation, and potential exposure.
repository: hashicorp/terraform
label: Security
language: Other
comments_count: 5
repository_stars: 45532
---

Always use modern identity-based authentication methods instead of static credentials when accessing external systems. This reduces security risks associated with credential management, rotation, and potential exposure.

For Azure resources, prefer authentication methods in this order:
1. OpenID Connect / Workload identity federation (recommended)
2. Managed Identities 
3. Azure Active Directory
4. Access Keys/SAS Tokens (avoid for new workloads)

```hcl
# Example - Using OpenID Connect for Azure authentication
terraform {
  backend "azurerm" {
    use_oidc             = true                                    # Enable OIDC authentication
    use_azuread_auth     = true                                    # Use Azure AD authentication
    tenant_id            = "00000000-0000-0000-0000-000000000000"  # Can be set via ARM_TENANT_ID
    client_id            = "00000000-0000-0000-0000-000000000000"  # Can be set via ARM_CLIENT_ID
    storage_account_name = "abcd1234"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

When executing commands or generating credentials:
1. Avoid using Terraform variables directly in command strings to prevent shell injection vulnerabilities
2. Use the `environment` parameter for variable substitution
3. Configure credential generation parameters to ensure both security and compatibility:

```hcl
# Generate a secure password with compatible special characters
ephemeral "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}
```