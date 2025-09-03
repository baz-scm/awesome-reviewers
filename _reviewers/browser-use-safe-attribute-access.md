---
title: Safe attribute access
description: Always use defensive programming patterns when accessing object attributes,
  especially when dealing with optional or potentially None values. Use hasattr()
  checks before accessing attributes, prefer public accessor methods over private
  attributes, and add null checks when accessing nested properties.
repository: browser-use/browser-use
label: Null Handling
language: Python
comments_count: 3
repository_stars: 69139
---

Always use defensive programming patterns when accessing object attributes, especially when dealing with optional or potentially None values. Use hasattr() checks before accessing attributes, prefer public accessor methods over private attributes, and add null checks when accessing nested properties.

Key patterns to follow:
1. Use hasattr() to check attribute existence before access
2. Prefer public accessor methods over direct private attribute access
3. Add null checks when accessing returned objects from methods
4. Understand the actual object structure before accessing nested properties

Example of unsafe vs safe access:
```python
# Unsafe - direct private attribute access
if hasattr(page.context, '_browser_context_config'):
    if hasattr(page.context._browser_context_config, 'anti_fingerprint'):
        self.anti_fingerprint = page.context._browser_context_config.anti_fingerprint

# Safe - public accessor with null checks
if hasattr(page, 'context') and hasattr(page.context, 'get_config'):
    config = page.context.get_config()
    if config is not None and hasattr(config, 'anti_fingerprint'):
        self.anti_fingerprint = config.anti_fingerprint
```

This approach prevents AttributeError exceptions, respects encapsulation, reduces coupling, and makes code more robust against null references and missing attributes.