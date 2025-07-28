---
title: avoid code duplication
description: Create reusable components instead of duplicating similar code patterns.
  When you find yourself writing similar classes, functions, or logic blocks, extract
  the common functionality into base classes, helper functions, or generic components
  that can be parameterized.
repository: home-assistant/core
label: Code Style
language: Python
comments_count: 8
repository_stars: 80450
---

Create reusable components instead of duplicating similar code patterns. When you find yourself writing similar classes, functions, or logic blocks, extract the common functionality into base classes, helper functions, or generic components that can be parameterized.

Examples of duplication to avoid:
- Multiple entity classes with similar structure - create a base entity class
- Repeated device info logic across platforms - move to shared base entity or helper function  
- Similar validation or processing logic - extract to utility functions in separate modules
- Multiple classes differing only in small details - create generic class with configurable descriptions

For instance, instead of creating separate button classes:
```python
class SetSleepTimerButton(ButtonEntity):
    # implementation

class ClearSleepTimerButton(ButtonEntity):  
    # similar implementation
```

Create a generic class with descriptions:
```python
class GenericButton(ButtonEntity):
    def __init__(self, description: ButtonEntityDescription):
        self.entity_description = description
        
    async def async_press(self) -> None:
        await self.entity_description.press_fn()
```

This approach improves maintainability, reduces bugs, and makes code more readable by eliminating repetitive patterns.