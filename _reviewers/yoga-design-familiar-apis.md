---
title: Design familiar APIs
description: Design APIs that align with platform conventions and user expectations
  rather than creating novel patterns. APIs should feel natural to developers already
  familiar with the target platform's idioms and established libraries.
repository: facebook/yoga
label: API
language: Other
comments_count: 3
repository_stars: 18255
---

Design APIs that align with platform conventions and user expectations rather than creating novel patterns. APIs should feel natural to developers already familiar with the target platform's idioms and established libraries.

When designing public interfaces, prioritize consistency with existing platform patterns over internal implementation convenience. For example, if your platform typically uses individual properties for layout values, follow that pattern even if it creates a larger API surface:

```objc
// Preferred: Matches UIKit conventions
@property (nonatomic) CGFloat paddingLeft;
@property (nonatomic) CGFloat paddingTop;
@property (nonatomic) CGFloat paddingStart; // RTL support

// Rather than novel approaches that break familiar patterns
- (void)setPadding:(CGFloat)padding forEdge:(YGEdge)edge;
```

Additionally, keep internal implementation details private. Helper functions and utilities should not be exposed in public headers just because they're convenient for internal use:

```cpp
// Wrong: Internal helpers in public API
template<typename T, typename... A>
T* YGAllocate(A&&... arguments) { /* internal helper */ }

// Right: Keep internal helpers in private headers
```

Make APIs explicit and unambiguous by requiring all necessary parameters rather than providing multiple variants. This forces developers to think about important decisions like units, reduces API surface area, and prevents ambiguous usage patterns.