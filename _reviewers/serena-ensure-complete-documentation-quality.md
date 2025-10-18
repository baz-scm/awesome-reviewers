---
title: Ensure complete documentation quality
description: 'Documentation should be comprehensive, clear, and provide all necessary
  context for understanding and using the code effectively. This includes several
  key aspects:'
repository: oraios/serena
label: Documentation
language: Python
comments_count: 4
repository_stars: 14465
---

Documentation should be comprehensive, clear, and provide all necessary context for understanding and using the code effectively. This includes several key aspects:

1. **Explain complex implementations**: When code uses non-standard approaches, tricks, or unexpected patterns, the docstring must explain what these are and why they're necessary. For example, if implementing custom handlers, loops, or configuration file writing, document the reasoning behind these choices.

2. **Use proper grammar and tone**: Documentation should use correct English grammar and maintain a professional, accurate tone. Avoid subjective or potentially misleading language like "quick and dirty" when describing legitimate implementation approaches.

3. **Include essential details**: Provide complete parameter information including units, types, and constraints. For example, specify whether a timeout parameter is in seconds, milliseconds, etc.

4. **Maintain consistency**: Follow established documentation standards and formats that support examples and are compatible with documentation tools.

Example of good documentation:
```python
def request_workspace_symbol(self, query: str, timeout: int = 30) -> Union[List[UnifiedSymbolInformation], None]:
    """
    Request symbols across the workspace using the Language Server Protocol.
    
    This method uses a custom retry mechanism with exponential backoff due to 
    server instability issues commonly seen with workspace symbol requests.
    
    :param query: The search string to filter symbols by
    :param timeout: Maximum wait time in seconds (default: 30)
    :return: List of matching symbols, or None if request fails
    """
```

This approach ensures that future developers can understand both what the code does and why it was implemented in a particular way.