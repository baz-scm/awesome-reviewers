---
title: Use descriptive identifiers
description: Choose clear, self-documenting names for variables, methods, parameters,
  and properties that explicitly convey their purpose and context. Avoid ambiguous
  or generic names that require additional context to understand.
repository: microsoft/terminal
label: Naming Conventions
language: C++
comments_count: 8
repository_stars: 99242
---

Choose clear, self-documenting names for variables, methods, parameters, and properties that explicitly convey their purpose and context. Avoid ambiguous or generic names that require additional context to understand.

Key principles:
- **Method names should include context**: Prefix methods with their domain (e.g., `_OnTabClick` instead of `_OnClick`)
- **Avoid magic parameters**: Replace boolean flags with descriptive method names (e.g., `SendKeyDownEvent()` instead of `SendKeyEvent(vkey, scanCode, flags, true)`)
- **Use meaningful parameter types**: Prefer enums over indices or magic numbers for better type safety and clarity
- **Variable names should reflect their actual content**: Use names that match the data type and purpose (e.g., `charSizeInDips` vs `charSizeInPixels`)
- **Property names should be specific**: Make property change notifications explicit about what changed

Example improvements:
```cpp
// Instead of:
_terminal->SendKeyEvent(vkey, scanCode, flags, true);
tabViewItem.PointerReleased({ this, &TerminalPage::_OnClick });

// Use:
_terminal->SendKeyDownEvent(vkey, scanCode, flags);
tabViewItem.PointerReleased({ this, &TerminalPage::_OnTabClick });

// Instead of:
double PaddingValueFromIndex(const winrt::hstring& paddingString, uint32_t paddingIndex)

// Use:
double PaddingValueFromIndex(const winrt::hstring& paddingString, PaddingDirection direction)
```

This approach reduces cognitive load, makes code self-documenting, and prevents misuse of APIs by making intent explicit through naming.