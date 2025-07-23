---
title: Prevent broken interactions
description: 'Ensure UI elements'' visual state (e.g., disabled, active) always matches
  their actual behavior. When an element appears disabled, completely prevent the
  associated actions by:'
repository: continuedev/continue
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 27819
---

Ensure UI elements' visual state (e.g., disabled, active) always matches their actual behavior. When an element appears disabled, completely prevent the associated actions by:

1. Blocking event handlers for disabled elements
2. Maintaining appropriate disabled states for features that would lead to broken experiences
3. Ensuring all user interaction methods (mouse, keyboard, programmatic) respect these constraints

This prevents users from encountering unexpected errors or broken states.

**Example fix:**
```tsx
// Before: UI looks disabled but handler still works
<div 
  className={`${disabled ? "cursor-not-allowed" : "cursor-pointer"}`}
  onClick={(e) => {
    dispatch(toggleToolSetting(props.tool.function.name));
    e.stopPropagation();
  }}
>

// After: Handler respects disabled state
<div 
  className={`${disabled ? "cursor-not-allowed" : "cursor-pointer"}`}
  onClick={(e) => {
    if (!disabled) {
      dispatch(toggleToolSetting(props.tool.function.name));
      e.stopPropagation();
    }
  }}
>
```

Similarly, when providing keyboard shortcuts or handlers (like Escape to close dialogs), ensure the handlers are accessible in all relevant contexts to prevent broken interaction patterns.