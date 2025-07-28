---
title: Use descriptive names
description: 'Avoid ambiguous or vague identifiers in favor of specific, self-documenting
  names that clearly convey purpose and context.


  Names should be immediately understandable without requiring additional context
  or documentation. Generic terms like "float" should be replaced with specific terms
  like "floatwin" or "win_float" to eliminate ambiguity. Function names...'
repository: neovim/neovim
label: Naming Conventions
language: C
comments_count: 4
repository_stars: 91433
---

Avoid ambiguous or vague identifiers in favor of specific, self-documenting names that clearly convey purpose and context.

Names should be immediately understandable without requiring additional context or documentation. Generic terms like "float" should be replaced with specific terms like "floatwin" or "win_float" to eliminate ambiguity. Function names should clearly indicate their action and scope.

Examples of improvements:
- `parse_float_option()` → `win_float_parse_option()` or `parse_previewpopup_option()`
- `get_current_prompt()` → `prompt_gettext()` or `prompt_cur_input()`
- Dictionary keys: `"wintype"` with value `"cmdwin"` instead of single-character codes
- API fields should be self-documenting: `wintype=="cmdwin"` is clearer than checking `strlen(wintype)==1`

This approach reduces cognitive load for developers, makes code more maintainable, and prevents confusion about identifier scope and purpose. When multiple similar functions exist, ensure names clearly distinguish their specific use cases rather than creating generic catch-all names.