---
title: Consistent terminology usage
description: Maintain consistent terminology and naming patterns throughout the codebase
  to avoid confusion and future conflicts. Use descriptive names that clearly indicate
  their purpose and remove unnecessary parameters or elements that don't serve a function.
repository: browser-use/browser-use
label: Naming Conventions
language: Python
comments_count: 3
repository_stars: 69139
---

Maintain consistent terminology and naming patterns throughout the codebase to avoid confusion and future conflicts. Use descriptive names that clearly indicate their purpose and remove unnecessary parameters or elements that don't serve a function.

Key principles:
- Keep consistent naming across the entire codebase, even if the underlying implementation might change
- Use semantic names that clearly describe the function or purpose (e.g., `on_step_start`/`on_step_end` instead of `before_step_func`/`after_step_func`)
- Remove unused parameters or fields that don't contribute to functionality
- Consider future extensibility when choosing terminology to avoid naming conflicts

Example from the discussions:
```python
# Good: Consistent terminology maintained across codebase
self.playwright = self.playwright or await self.playwright.chromium.connect_over_cdp(...)

# Avoid: Introducing conflicting terminology
self.driver = self.driver or await self.playwright.chromium.connect_over_cdp(...)

# Good: Descriptive parameter names
async def run(
    self,
    max_steps: int = 100,
    on_step_start: AgentHookFunc | None = None,
    on_step_end: AgentHookFunc | None = None
):

# Good: Remove unused parameters
class ExtractElementHtmlAction(BaseModel):
    index: int
    format: Literal['text', 'markdown', 'html'] = 'html'
    # xpath removed as it wasn't being used
```

This approach prevents terminology conflicts, improves code readability, and makes the codebase more maintainable by ensuring names accurately reflect their purpose and usage.