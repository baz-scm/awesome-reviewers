---
title: Use environment variables
description: When working with configurations that require sensitive data (credentials,
  tokens, passwords), always use environment variables instead of hardcoding values
  directly in configuration files. This prevents sensitive information from being
  stored in version control systems, state files, or plan outputs.
repository: hashicorp/terraform
label: Configurations
language: Other
comments_count: 21
repository_stars: 45532
---

When working with configurations that require sensitive data (credentials, tokens, passwords), always use environment variables instead of hardcoding values directly in configuration files. This prevents sensitive information from being stored in version control systems, state files, or plan outputs.

For backend configurations:
```hcl
terraform {
  backend "azurerm" {
    storage_account_name = "abcd1234"                              
    container_name       = "tfstate"                               
    key                  = "prod.terraform.tfstate"                
    # BAD: client_secret = "highly-sensitive-value"
    # GOOD: Use environment variable ARM_CLIENT_SECRET instead
  }
}
```

For write-only arguments and ephemeral resources, the same principle applies:
```hcl
resource "aws_db_instance" "example" {
  instance_class      = "db.t3.micro"
  allocated_storage   = "5"
  engine              = "postgres"
  username            = "example"
  skip_final_snapshot = true
  
  # Instead of hardcoding: password_wo = "secret-password"
  # Use an ephemeral resource with environment variables
  password_wo         = ephemeral.random_password.db_password.result
  password_wo_version = 1
}
```

This approach improves security by:
1. Keeping sensitive data out of version control repositories
2. Preventing exposure in Terraform's state and plan files
3. Allowing for different credentials in different environments
4. Enabling safer CI/CD pipelines with environment-specific secrets

Most providers support environment variable alternatives for sensitive configuration values - consult the provider documentation for the specific environment variable names available.