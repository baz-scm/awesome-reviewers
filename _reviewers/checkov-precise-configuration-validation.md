---
title: Precise configuration validation
description: 'Ensure configuration validation logic accurately reflects security intentions
  and best practices. When writing validation checks:


  1. Use precise operators that directly verify the intended state:'
repository: bridgecrewio/checkov
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 7667
---

Ensure configuration validation logic accurately reflects security intentions and best practices. When writing validation checks:

1. Use precise operators that directly verify the intended state:
   - For prohibited settings, check they "not_exist" rather than checking existence and then value
   - For boolean flags, verify the exact expected value (e.g., `not_equals_ignore_case "true"`) 
   - For resources that should have valid values, check "not_empty" rather than just "exists"

2. Account for dependencies between configuration settings:
   - If one setting makes another irrelevant, handle that case explicitly
   - Use logical operators (AND, OR) to represent these relationships accurately

Example:
```yaml
# GOOD: Directly validates the intended state
- cond_type: attribute
  attribute: "enable_feature"
  operator: "not_equals_ignore_case"
  value: "true"

# BAD: Unnecessarily complex and error-prone
- cond_type: attribute
  attribute: "enable_feature"
  operator: "exists"
- cond_type: attribute
  attribute: "enable_feature"
  operator: "equals_ignore_case"
  value: "false"

# GOOD: Handles configuration dependencies
- or:
  - cond_type: attribute
    attribute: "shared_access_key_enabled"
    operator: "equals_ignore_case" 
    value: "false"
  - and:
    - cond_type: attribute
      attribute: "shared_access_key_enabled"
      operator: "equals_ignore_case"
      value: "true"
    - cond_type: attribute
      attribute: "sas_policy.expiration_period"
      operator: "exists"
```