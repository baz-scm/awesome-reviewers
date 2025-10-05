---
title: understand undefined value semantics
description: Before modifying initialization patterns or removing static variables,
  investigate the semantic meaning of undefined values and object lifetimes in the
  existing codebase. What appears to be a memory leak or improper initialization may
  be intentional design.
repository: facebook/yoga
label: Null Handling
language: C++
comments_count: 2
repository_stars: 18255
---

Before modifying initialization patterns or removing static variables, investigate the semantic meaning of undefined values and object lifetimes in the existing codebase. What appears to be a memory leak or improper initialization may be intentional design.

Key considerations:
- Static variables with process lifetime are not memory leaks
- Undefined values (like `YGUndefined`) may be semantically different from zero initialization
- Prefer proper C++ initialization over manual memory operations, but verify behavioral compatibility

Example of proper investigation:
```cpp
// Before changing this:
static YGConfigRef defaultConfig = YGConfigNew();  // Not a leak - process lifetime

// Or this:
memset(&(node->getLayout()), 0, sizeof(YGLayout));

// Investigate: Does the constructor initialize differently?
node->getLayout() = {};  // May initialize with YGUndefined instead of 0
// If tests break, understand why before forcing zero values
```

Always verify that your changes preserve the intended semantics, especially when dealing with undefined states, static lifetimes, or special sentinel values.