---
title: validate algorithmic inputs
description: Always validate inputs and handle edge cases before performing algorithmic
  operations, especially when dealing with indices, state transitions, or data structure
  traversals. Check for boundary conditions, invalid states, and null/undefined values
  that could cause out-of-bounds access or undefined behavior.
repository: tree-sitter/tree-sitter
label: Algorithms
language: Other
comments_count: 2
repository_stars: 21799
---

Always validate inputs and handle edge cases before performing algorithmic operations, especially when dealing with indices, state transitions, or data structure traversals. Check for boundary conditions, invalid states, and null/undefined values that could cause out-of-bounds access or undefined behavior.

Key practices:
- Validate array indices before access
- Check for special sentinel values (like -1 or null states)
- Ensure required fields exist before using them
- Handle empty or invalid input gracefully

Example from parse table operations:
```cpp
// Before: Direct access without validation
*state_index = new_state_ids[*state_index];

// After: Validate before accessing
if (*state_index != (ParseStateId)(-1))
  *state_index = new_state_ids[*state_index];

// Also ensure meaningful fields exist
if ((action.type == ParseActionTypeShift && !action.extra) || 
    action.type == ParseActionTypeRecover)
  fn(&action.state_index);
```

This prevents crashes from invalid indices and ensures algorithms only operate on valid data, making code more robust and maintainable.