---
title: Use semantic naming
description: Names should clearly communicate their purpose, type, and behavior to
  improve code maintainability and accessibility. Avoid misleading or ambiguous terminology
  that can confuse developers or users.
repository: microsoft/terminal
label: Naming Conventions
language: Other
comments_count: 12
repository_stars: 99242
---

Names should clearly communicate their purpose, type, and behavior to improve code maintainability and accessibility. Avoid misleading or ambiguous terminology that can confuse developers or users.

Key principles:
- **Indicate type and purpose**: Variable names should reflect both what they contain and how they're used. For example, prefer `ProposedShortcutActionName` over `ProposedShortcutAction` when the value is specifically a string.
- **Avoid misleading terms**: Don't use names like `required` for validation checks when it's not actually a boolean requirement flag.
- **Provide accessibility context**: UI elements must have meaningful names for screen readers. Set `AutomationProperties.Name` with descriptive text rather than leaving buttons to be read as just "button".
- **Prefer positive naming**: Use `ScrollToZoom` instead of `DisableMouseZoom` to avoid double negatives and improve clarity.
- **Follow consistent capitalization**: Use sentence case for UI text ("Split pane down" not "Split Pane Down") and maintain consistency across similar elements.

Example of improved naming:
```cpp
// Before: misleading parameter name
#define DECLARE_ARGS(type, name, jsonKey, required, ...) 
// 'required' is actually a validation expression, not a boolean

// After: clearer parameter name  
#define DECLARE_ARGS(type, name, jsonKey, validation, ...)
// 'validation' clearly indicates this is a validation expression

// Before: unclear type
VIEW_MODEL_OBSERVABLE_PROPERTY(IInspectable, ProposedShortcutAction);

// After: type-indicating name
VIEW_MODEL_OBSERVABLE_PROPERTY(IInspectable, ProposedShortcutActionName);
```

This approach reduces cognitive load, improves accessibility, and makes code self-documenting.