---
title: no braces short ifs
description: Remove braces around single-statement if blocks to maintain consistent
  code style and improve readability. This applies to all control flow statements
  with single statements, including if, else if, and else blocks.
repository: hyprwm/Hyprland
label: Code Style
language: C++
comments_count: 17
repository_stars: 28863
---

Remove braces around single-statement if blocks to maintain consistent code style and improve readability. This applies to all control flow statements with single statements, including if, else if, and else blocks.

The codebase follows a consistent style where braces are omitted for single-statement conditionals. This reduces visual clutter and maintains consistency across the project.

**Examples:**

❌ Avoid:
```cpp
if (condition) {
    return;
}

if (pWindow) {
    pWindow->close();
}
```

✅ Prefer:
```cpp
if (condition)
    return;

if (pWindow)
    pWindow->close();
```

**Exception:** Keep braces when the statement spans multiple lines or when it improves clarity in complex nested conditions.

This rule helps maintain visual consistency throughout the codebase and follows the established project conventions. Apply this consistently across all new code and when modifying existing code.