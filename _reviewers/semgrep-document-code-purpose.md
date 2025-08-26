---
title: Document code purpose
description: Ensure that code elements have clear documentation explaining their purpose,
  behavior, and context. This includes function parameters (especially non-obvious
  ones), complex business logic, and magic values or constants.
repository: semgrep/semgrep
label: Documentation
language: Python
comments_count: 4
repository_stars: 12598
---

Ensure that code elements have clear documentation explaining their purpose, behavior, and context. This includes function parameters (especially non-obvious ones), complex business logic, and magic values or constants.

Key areas to document:
- **Function parameters**: Add docstrings or comments explaining what parameters do, when they should be used, and their expected behavior
- **Complex logic**: Add explanatory comments before or within complex code sections that describe what the code does and why it's necessary
- **Magic values**: Document the source, purpose, and meaning of hardcoded strings, numbers, or constants

Example from the discussions:
```python
def add_engine_config(
    self, engineType: "EngineType", secrets_origins: Optional[str]
) -> None:
    """
    Configure engine with type and secrets information.
    
    Args:
        engineType: The type of engine to configure
        secrets_origins: Source information for secrets detection, 
                        e.g., "github" or "local_scan"
    """
```

This practice helps future developers (including yourself) understand the intent behind code decisions and reduces the cognitive load when maintaining or extending the codebase.