---
title: API clarity over convenience
description: When designing APIs, prioritize clarity and self-documentation over implementation
  convenience. Choose interface patterns that make the code's intent immediately obvious
  to consumers and debuggers.
repository: microsoft/terminal
label: API
language: Other
comments_count: 2
repository_stars: 99242
---

When designing APIs, prioritize clarity and self-documentation over implementation convenience. Choose interface patterns that make the code's intent immediately obvious to consumers and debuggers.

For data access APIs, prefer descriptive string-based keys over numerical indexing when the performance impact is acceptable. As noted in code review discussions: "If you were to debug it and see '5' it's not immediately clear what you want, whereas with 'windowTitle' you kind of know already."

For interface definitions, avoid unnecessary annotations that add complexity without benefit. Only use attributes like `[default_interface]` when the runtime class has no other interface and no identifying characteristics.

Example of preferred approach:
```cpp
// Instead of numerical indexing:
GetArgAt(5)  // Unclear what argument this represents

// Prefer descriptive access:
GetArgByName("windowTitle")  // Self-documenting intent

// Or return descriptors that include names:
auto descriptor = GetArgDescriptorAt(index);  // descriptor.Name provides context
```

This principle applies broadly to API design: choose patterns that make debugging easier and code more self-documenting, even if they require slightly more implementation effort.