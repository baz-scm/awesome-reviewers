---
title: Clarify test documentation
description: Ensure all testing-related documentation is clear, accurate, and user-focused.
  Use precise terminology when describing test components, fully explain configuration
  attributes with their effects, and provide complete examples that demonstrate proper
  usage.
repository: hashicorp/terraform
label: Testing
language: Other
comments_count: 4
repository_stars: 45532
---

Ensure all testing-related documentation is clear, accurate, and user-focused. Use precise terminology when describing test components, fully explain configuration attributes with their effects, and provide complete examples that demonstrate proper usage.

When documenting test blocks and attributes:
- Use exact parameter names and describe their full behavior
- Explain default values and all possible options
- Reference related sections for context

For example:

```hcl
test "configuration_example" {
  # Document that this enables parallel execution of all run blocks
  # within this test unless specifically overridden
  parallel = true
}

run "validate_resource_properties" {
  # Document that this block contains validation logic
  # with clear explanation of the condition and error message
  condition     = local.resource_name != ""
  error_message = "Resource name cannot be empty"
}
```

Well-documented tests serve as both validation tools and self-explanatory examples, making your codebase more maintainable and helping new team members understand testing requirements quickly.