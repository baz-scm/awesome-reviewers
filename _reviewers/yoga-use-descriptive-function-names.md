---
title: Use descriptive function names
description: Function names should clearly convey their purpose and behavior, not
  just their signature or implementation details. Avoid names that could be confused
  with existing functions that have similar but different behavior.
repository: facebook/yoga
label: Naming Conventions
language: C
comments_count: 2
repository_stars: 18255
---

Function names should clearly convey their purpose and behavior, not just their signature or implementation details. Avoid names that could be confused with existing functions that have similar but different behavior.

When naming functions, consider what the function actually accomplishes rather than how it accomplishes it. For example, `YGValueToFloat` describes the conversion but not the purpose, while `YGValueResolve` better describes what the function is trying to achieve.

Additionally, be careful when adding functions with similar names to existing ones. If `YGNodeMarkDirtyInternal` already handles recursion, naming another function `YGNodeMarkDirtyRecursive` creates confusion about which function to use and their behavioral differences.

Example of improvement:
```c
// Less descriptive - focuses on conversion
static inline float YGValueToFloat(const YGValue unit, const float parentSize)

// More descriptive - focuses on purpose  
static inline float YGValueResolve(const YGValue unit, const float parentSize)
```