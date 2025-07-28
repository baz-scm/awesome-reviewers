---
title: prefer explicit code
description: Write code that explicitly states its intent rather than relying on implicit
  behavior or complex constructs. This improves readability and maintainability by
  making the code's purpose immediately clear to other developers.
repository: facebook/react-native
label: Code Style
language: C++
comments_count: 2
repository_stars: 123178
---

Write code that explicitly states its intent rather than relying on implicit behavior or complex constructs. This improves readability and maintainability by making the code's purpose immediately clear to other developers.

Key practices:
- Set default values explicitly instead of using empty initializers like `{}`
- Structure conditional logic with clear if-else blocks rather than complex ternary operations or intermediate variables
- Add intent-clarifying comments when the logic serves multiple purposes

Example of explicit default values:
```cpp
// Prefer explicit default
disableKeyboardShortcuts(convertRawProp(
    context,
    rawProps,
    "disableKeyboardShortcuts",
    sourceProps.disableKeyboardShortcuts,
    {false}))  // explicit default value

// Instead of implicit empty default
disableKeyboardShortcuts(convertRawProp(
    context,
    rawProps,
    "disableKeyboardShortcuts",
    sourceProps.disableKeyboardShortcuts,
    {}))  // unclear what the default is
```

Example of clear conditional structure:
```cpp
// Prefer clear if-else structure
if (ignoreYogaStyleProps_ || filterObjectKeys != nullptr) {
  // We need to filter props
  return jsi::dynamicFromValue(*runtime_, value_, [&](const std::string& key) {
    if (ignoreYogaStyleProps_ && isYogaStyleProp(key)) {
      return false;
    }
    if (filterObjectKeys) {
      return filterObjectKeys(key);
    }
    return true;
  });
} else {
  // We don't need to filter, just include all props by default
  return jsi::dynamicFromValue(*runtime_, value_, nullptr);
}

// Instead of complex ternary with intermediate variables
const std::function<bool(const std::string&)> filterFunctionOrNull =
    ignoreYogaStyleProps_ || filterObjectKeys != nullptr
    ? propFilterFunction
    : nullptr;
return jsi::dynamicFromValue(*runtime_, value_, filterFunctionOrNull);
```