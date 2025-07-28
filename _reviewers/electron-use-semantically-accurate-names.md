---
title: Use semantically accurate names
description: Choose parameter and method names that accurately reflect their semantic
  meaning and implementation reality, rather than names that may be misleading or
  platform-specific.
repository: electron/electron
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 117644
---

Choose parameter and method names that accurately reflect their semantic meaning and implementation reality, rather than names that may be misleading or platform-specific.

Avoid names that imply specific technical requirements when the actual implementation is more flexible. For example, a parameter named `guid` suggests it must be a GUID format, when the implementation may accept any unique string identifier.

Similarly, method names should accurately describe their action. Names like `evaluate` can be misleading if they suggest using `eval()` when the actual implementation executes code differently.

Examples of improvements:
- `guid` → `identifier` (when the parameter accepts any unique string, not just GUIDs)
- `roundedCorner` → `roundedCorners` (when the property affects multiple corners)
- `evaluateInMainWorld` → `executeScriptInMainWorld` (when the method executes rather than evaluates code)

This principle helps prevent developer confusion and makes APIs more intuitive across different platforms and use cases.