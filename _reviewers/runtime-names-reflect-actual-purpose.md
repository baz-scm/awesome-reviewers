---
title: Names reflect actual purpose
description: Name variables, properties, and functions to accurately reflect their
  purpose and actual usage in code, not just their technical classification. This
  ensures other developers can understand the intent without having to analyze implementation
  details.
repository: dotnet/runtime
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 16578
---

Name variables, properties, and functions to accurately reflect their purpose and actual usage in code, not just their technical classification. This ensures other developers can understand the intent without having to analyze implementation details.

**Key guidelines:**
- Choose names that describe what the element is used for rather than its internal structure
- For user-facing configurations, balance technical precision with understandable terminology
- When renaming elements, verify their actual usage rather than assuming based on similar patterns

**Example:**
```csharp
// Avoid misleading names
var _maskData = new int[size]; // Not actually used as a mask

// Better - name reflects actual usage
var _selectParameters = new int[size]; // Used as parameters in select operations

// For configurations, prefer descriptive names over technical terms
// Less clear for users:
options.WasmEnableEventPipe = true;

// More descriptive of purpose:
options.WasmEnablePerformanceTracing = true;
```

Follow this principle even when a name seems technically correct - what matters is whether it effectively communicates how the element is actually used in your codebase.
