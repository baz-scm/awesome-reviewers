---
title: API input/output validation
description: Ensure robust parsing of API inputs and proper formatting of outputs
  to prevent parsing errors and unexpected behavior. API implementations must handle
  edge cases where command identifiers might appear within parameter values, and all
  output formats must properly escape special characters.
repository: hyprwm/Hyprland
label: API
language: C++
comments_count: 2
repository_stars: 28863
---

Ensure robust parsing of API inputs and proper formatting of outputs to prevent parsing errors and unexpected behavior. API implementations must handle edge cases where command identifiers might appear within parameter values, and all output formats must properly escape special characters.

For input parsing, avoid simple substring matching that could incorrectly identify commands within parameter data. For example, a command like `/notify blah blah /decorations` should be parsed as the `/notify` command with `/decorations` as part of the parameter string, not as a `/decorations` command.

For output formatting, always escape special characters in structured formats like JSON:

```cpp
// Bad - missing escaping
result += std::format(R"#("{}",)#", current);

// Good - with proper escaping  
result += std::format(R"#("{}",)#", escapeJSONStrings(current));
```

This prevents client-side parsing failures when API responses contain quotes, newlines, or other special characters. Implement comprehensive input validation and output sanitization as fundamental requirements for all API endpoints.