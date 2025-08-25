---
title: Follow established naming conventions
description: Adhere to established naming conventions consistently throughout the
  codebase, prioritizing official documentation standards when available. Use appropriate
  case conventions (ALL_CAPS for constants, descriptive names for variables) and maintain
  consistency with external API standards.
repository: bytedance/trae-agent
label: Naming Conventions
language: Python
comments_count: 2
repository_stars: 9088
---

Adhere to established naming conventions consistently throughout the codebase, prioritizing official documentation standards when available. Use appropriate case conventions (ALL_CAPS for constants, descriptive names for variables) and maintain consistency with external API standards.

When naming conflicts arise between internal consistency and official documentation, prefer the official documentation approach. For constants, use ALL_CAPS to clearly indicate their global scope and immutable nature.

Examples:
```python
# Good: Constant with proper naming
MODEL_PARAMETERS = ModelParameters(...)

# Good: API key following official documentation
API_KEY = os.getenv("GEMINI_API_KEY")  # Following Google's official docs

# Avoid: Inconsistent constant naming
model_parameters = ModelParameters(...)

# Avoid: Internal naming that conflicts with official docs
API_KEY = os.getenv("GOOGLE_API_KEY")  # When official docs specify GEMINI_API_KEY
```

This approach enhances code readability, reduces confusion for new team members, and ensures compatibility with external documentation and examples.