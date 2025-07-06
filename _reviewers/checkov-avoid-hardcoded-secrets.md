---
title: Avoid hardcoded secrets
description: Never hardcode sensitive information like passwords, API keys, or other
  secrets directly in infrastructure code. These secrets can be exposed through version
  control systems, putting your infrastructure at risk.
repository: bridgecrewio/checkov
label: Security
language: Terraform
comments_count: 1
repository_stars: 7667
---

Never hardcode sensitive information like passwords, API keys, or other secrets directly in infrastructure code. These secrets can be exposed through version control systems, putting your infrastructure at risk.

Instead:
1. Use secret management solutions (Azure Key Vault, HashiCorp Vault, etc.)
2. Reference environment variables or secure input variables
3. For Terraform specifically, utilize tfvars files (kept outside of version control)
4. Consider using dynamic providers that can fetch secrets at runtime

When testing infrastructure code that requires secrets, use placeholder values and clearly annotate them with security scan exemptions:

```hcl
container {
  # Other configuration...
  
  secure_environment_variables = {
    API_KEY = var.api_key  # Proper approach: using a variable
    # Instead of hardcoding: API_KEY = "actual-secret-value"
    
    # For test environments only:
    TEST_SECRET = "dummy-value"  # checkov:skip=CKV_SECRET_6 test environment only
  }
}
```

Regularly audit your code for hardcoded secrets using security scanning tools like Checkov as part of your CI/CD pipeline.