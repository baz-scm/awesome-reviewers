---
title: Meaningful consistent naming
description: 'Use names that clearly describe the purpose and behavior of variables,
  methods, classes, and files, while maintaining consistency across the codebase.
  Follow these guidelines:'
repository: prowler-cloud/prowler
label: Naming Conventions
language: Python
comments_count: 7
repository_stars: 11834
---

Use names that clearly describe the purpose and behavior of variables, methods, classes, and files, while maintaining consistency across the codebase. Follow these guidelines:

1. **Be semantically accurate**: Names should reflect their exact purpose and behavior.
   - Name methods according to what they do: use 'get_' for retrieval and 'set_' for modification.
   - Example: Rename `get_required_permissions` to `set_required_permissions` if the method is setting values.

2. **Maintain consistency**: Use consistent patterns and terminology throughout the codebase.
   - Apply consistent suffixes for related functions (e.g., all task functions should end with `_task`).
   - Use consistent placeholder values (e.g., always use 'N/A' for missing values instead of arbitrary values like 'NoName').
   - Stick to the same terminology for similar concepts (use either 'report' or 'output' consistently, not both).

3. **Follow established conventions**: Adhere to language and framework-specific naming standards.
   - Use singular nouns for model class names (e.g., 'SAMLConfiguration' not 'SAMLConfigurations').
   - Choose descriptive variable names that distinguish similar concepts (e.g., `api_token` vs generic `token`).
   - Avoid ambiguous names that could cause confusion (e.g., prefer `legacy_auth_enabled` over `modern_authentication` when the value represents legacy authentication).