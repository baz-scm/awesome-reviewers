---
title: prefer simple code patterns
description: Choose straightforward, readable code patterns over complex or clever
  alternatives. This improves maintainability and reduces cognitive load for other
  developers.
repository: sveltejs/svelte
label: Code Style
language: JavaScript
comments_count: 9
repository_stars: 83580
---

Choose straightforward, readable code patterns over complex or clever alternatives. This improves maintainability and reduces cognitive load for other developers.

**Key principles:**
- Use direct boolean methods instead of complex expressions: `array.some(condition)` instead of `array.find(condition) !== null`
- Prefer simple conditional operators: `value && expression` instead of `value ? expression : null` when appropriate
- Use explicit control structures over indirection: direct `switch` statements instead of mapping objects when the logic is clearer
- Choose appropriate data types: booleans for binary states instead of numeric flags, specific types when mutation isn't needed
- Avoid unnecessary complexity: split complex expressions across lines rather than using comma operators or complex casting

**Example:**
```javascript
// Complex/clever approach
const result = items.find(item => item.active) !== null ? processItems() : null;
const status = flags & DIRTY_FLAG !== 0 ? 1 : 0;

// Simple, readable approach  
const hasActiveItem = items.some(item => item.active);
if (hasActiveItem) {
  processItems();
}
const isDirty = (flags & DIRTY_FLAG) !== 0;
```

The goal is code that can be quickly understood by any team member, even when they're unfamiliar with the specific context or under time pressure.