---
title: Avoid hardcoded secrets
description: Never include hardcoded secrets or credentials in your infrastructure
  as code files. Secrets in configuration files pose significant security risks as
  they may be inadvertently exposed through version control systems or shared repositories.
repository: bridgecrewio/checkov
label: Security
language: Terraform
comments_count: 1
repository_stars: 7668
---

Never include hardcoded secrets or credentials in your infrastructure as code files. Secrets in configuration files pose significant security risks as they may be inadvertently exposed through version control systems or shared repositories.

Instead:
- Use secret management services like Azure Key Vault, HashiCorp Vault, or AWS Secrets Manager
- Reference environment variables or other external sources
- Utilize native secret handling mechanisms in your infrastructure platforms

When writing Terraform configurations for Azure Container Instances, use variable references instead of hardcoded values:

```hcl
# BAD PRACTICE - Hardcoded secret
resource "azurerm_container_group" "example" {
  # other configuration...
  
  container {
    # other settings...
    
    secure_environment_variables = {
      API_KEY = "actual-secret-value-here"  # Security risk!
    }
  }
}

# GOOD PRACTICE - Referenced secret
variable "api_key" {
  description = "API key for the container"
  sensitive   = true  # Marks as sensitive in Terraform
}

resource "azurerm_container_group" "example" {
  # other configuration...
  
  container {
    # other settings...
    
    secure_environment_variables = {
      API_KEY = var.api_key
    }
  }
}
```

For testing scenarios where you need placeholder secrets, use clearly marked test values and include security check exceptions:

```hcl
secure_environment_variables = {
  TEST_API_KEY = "test-value-only"  # checkov:skip=CKV_SECRET_6 test-only secret
}
```