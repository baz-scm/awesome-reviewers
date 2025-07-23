---
title: Externalize configuration values
description: Always externalize configuration values rather than hardcoding them directly
  in the code. This improves maintainability, enables easier configuration changes,
  and ensures consistency across the codebase.
repository: Aider-AI/aider
label: Configurations
language: Python
comments_count: 4
repository_stars: 35856
---

Always externalize configuration values rather than hardcoding them directly in the code. This improves maintainability, enables easier configuration changes, and ensures consistency across the codebase.

Key practices:
1. Replace hardcoded strings with values retrieved from a centralized configuration system
2. Ensure the correct configuration keys are used for specific components
3. Use standardized utility functions that honor user configuration settings

Example:
```python
# Instead of this:
main_system = """Act as an expert software developer."""

# Do this:
from . import prompt_manager
yaml_prompt_entry = prompt_manager.get_prompt_value('ComponentName', 'main_system')

# And when reading files, respect user configuration:
# Instead of:
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()
    
# Use utilities that honor user settings:
content = io.read_text(file_path)  # Respects --encoding setting
```

This approach makes the codebase more flexible, easier to maintain, and respectful of user-defined settings.