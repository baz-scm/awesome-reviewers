---
title: Safe optional handling
description: Always use safe patterns when working with optional, nullable, or potentially
  empty types. Avoid direct comparisons with optional values and ensure proper initialization
  of nullable members.
repository: microsoft/terminal
label: Null Handling
language: C++
comments_count: 4
repository_stars: 99242
---

Always use safe patterns when working with optional, nullable, or potentially empty types. Avoid direct comparisons with optional values and ensure proper initialization of nullable members.

Key practices:
- Use `.value_or(default)` instead of direct comparisons with optional types
- Initialize nullable member variables explicitly (e.g., `_richBlock{ nullptr }`)
- Check for null/empty state before dereferencing (use ternary operators when needed)
- Be cautious with move operations that may leave objects in empty states

Example of unsafe vs safe optional handling:
```cpp
// Unsafe - direct comparison with optional
if (modernValue == 1u) // optional<uint32_t> != uint32_t comparison

// Safe - use value_or for truthy check
if (modernValue.value_or(0) != 0)

// Unsafe - assuming non-null without check
theme.Pane().ActiveBorderColor() // crashes if Pane() returns null

// Safe - null check with ternary
const auto paneActiveBorderColor = theme.Pane() ? theme.Pane().ActiveBorderColor() : nullptr;
```

This prevents crashes from null dereferences, undefined behavior from uninitialized members, and logic errors from improper optional comparisons.