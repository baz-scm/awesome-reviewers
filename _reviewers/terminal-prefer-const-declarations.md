---
title: prefer const declarations
description: Use `const` for variables that are not modified after initialization,
  and avoid creating unnecessary temporary variables when the value can be computed
  directly in the declaration.
repository: microsoft/terminal
label: Code Style
language: C++
comments_count: 5
repository_stars: 99242
---

Use `const` for variables that are not modified after initialization, and avoid creating unnecessary temporary variables when the value can be computed directly in the declaration.

This improves code clarity by making immutability explicit and reduces cognitive load by eliminating intermediate variables that don't add semantic value.

**Examples:**

```cpp
// Preferred
const auto paneActiveBorderColor = theme.Pane() ? theme.Pane().ActiveBorderColor() : nullptr;
const auto setter = setterBase.as<winrt::Windows::UI::Xaml::Setter>();
const auto property = setter.Property();

// Avoid
auto paneActiveBorderColor = theme.Pane() ? theme.Pane().ActiveBorderColor() : nullptr;
const bool isAudibleSet = WI_IsFlagSet(bellStyle, BellStyle::Audible);
const bool isWindowSet = WI_IsFlagSet(bellStyle, BellStyle::Window);
// ... later using these bools
if (isAudibleSet && isWindowSet) // Instead, use direct flag checks
```

For parameter passing, prefer `const&` over copying when the parameter won't be modified, or use move semantics when transferring ownership. Avoid the `auto{}` brace-initialization syntax as it can be brittle and is not widely adopted in the ecosystem.