---
title: Validate configurations correctly
description: When writing validation logic for configurations, ensure you're using
  the appropriate operators that correctly test for the intended state. Incorrect
  validation operators can lead to false results and security vulnerabilities.
repository: bridgecrewio/checkov
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 7668
---

When writing validation logic for configurations, ensure you're using the appropriate operators that correctly test for the intended state. Incorrect validation operators can lead to false results and security vulnerabilities.

Common mistakes include:

1. Using `exists` when you should check that a value is not empty
2. Using `length_greater_than` when you should use `not_exists` to verify absence
3. Using `equals_ignore_case` with the wrong comparison value

Example - Incorrect:
```yaml
- cond_type: attribute
  resource_types: "google_container_cluster"
  attribute: "enable_kubernetes_alpha"
  operator: "equals_ignore_case"  # This doesn't specify what value it should equal
```

Correct:
```yaml
- cond_type: attribute
  resource_types: "google_container_cluster"
  attribute: "enable_kubernetes_alpha"
  operator: "not_equals_ignore_case"
  value: "true"  # Now it correctly checks that alpha cluster feature is disabled
```

When validating network configurations, similarly ensure your logic matches your security intent:
```yaml
# Incorrect - checks length rather than absence
- cond_type: attribute
  resource_types: ["azurerm_network_interface"]
  attribute: "ip_configuration.public_ip_address_id"
  operator: "length_greater_than"  # Wrong operator for checking absence
  value: 0

# Correct - properly checks for absence
- cond_type: attribute
  resource_types: ["azurerm_network_interface"]
  attribute: "ip_configuration.public_ip_address_id"
  operator: "not_exists"  # Correctly checks that public IP is not configured
```

Always consider what exactly your validation is trying to check and select operators that precisely match that intention.