---
title: Use descriptive consistent names
description: Choose names that are both semantically accurate and consistent with
  established patterns. Names should clearly convey their purpose, data type, and
  behavior while following existing conventions in the codebase and upstream dependencies.
repository: electron/electron
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 117644
---

Choose names that are both semantically accurate and consistent with established patterns. Names should clearly convey their purpose, data type, and behavior while following existing conventions in the codebase and upstream dependencies.

Key principles:
- Use descriptive names that eliminate ambiguity about purpose (e.g., `CheckSwitchNameValid` returning an error message vs `IsSwitchNameValid` returning boolean)
- Match variable names to their data structure (e.g., `reasons` for a vector, not `reason`)
- Maintain consistent casing and formatting patterns within the same file or module
- Follow established external conventions when available (e.g., Chromium's "Fullscreen" as one word)
- Avoid names that could conflict with existing or future identifiers

Example:
```cpp
// Better: Descriptive and indicates return type
std::optional<std::string_view> CheckSwitchNameValid(std::string_view key) {
  if (!std::ranges::none_of(key, absl::ascii_isupper))
    return "Switch name must be lowercase";
  return {};
}

// Better: Plural name for collection parameter
void OnWindowEndSession(const std::vector<std::string> reasons) {
  // ...
}
```