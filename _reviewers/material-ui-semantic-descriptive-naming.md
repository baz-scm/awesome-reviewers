---
title: Semantic descriptive naming
description: Choose names that clearly communicate purpose, behavior, and semantics
  of code elements. Names should be self-explanatory and convey their intended functionality
  without requiring additional context.
repository: mui/material-ui
label: Naming Conventions
language: JavaScript
comments_count: 4
repository_stars: 96063
---

Choose names that clearly communicate purpose, behavior, and semantics of code elements. Names should be self-explanatory and convey their intended functionality without requiring additional context.

**Guidelines:**

1. **Use semantic names for HTML elements and attributes**
   - Assign proper ARIA roles that match component functionality (e.g., `role="switch"` for toggle components)
   - This enhances accessibility and code clarity

2. **Create descriptive UI labels and tooltips**
   - Prefer specific, action-oriented labels over generic ones
   - Example: "Open standalone demo" is clearer than "Open in new tab"

3. **Choose component and function names that indicate behavior and limitations**
   - If a function has specific trade-offs or constraints, reflect this in its name
   - Example: Prefix with "fast" when performance is prioritized over complete correctness
   ```javascript
   // Good: Name indicates performance optimization with potential limitations
   import fastDeepAssign from '@mui/utils/fastDeepAssign';
   
   // Alternative: More generic name requires additional documentation
   import deepAssign from '@mui/utils/deepAssign';
   ```

4. **Use consistent naming patterns for component props**
   - Select prop names that clearly indicate their purpose
   - Follow established naming conventions within your codebase
   - Example: For props that modify component behavior, use descriptive prefixes:
   ```jsx
   // Clear naming pattern for skipping option highlight
   <MenuItem muiSkipOptionHighlight>Skip highlight</MenuItem>
   ```

When choosing between multiple naming options, prioritize clarity and predictability over brevity. Well-named elements reduce the need for comments and make code more maintainable.