---
title: Add safety checks
description: Always add appropriate safety checks before operations that could result
  in undefined behavior, null references, or memory issues. This includes using weak
  references to prevent retain cycles, verifying exact object types before type-specific
  operations, and adding conditional checks before calling methods that may return
  undefined values.
repository: facebook/yoga
label: Null Handling
language: Objective-C
comments_count: 3
repository_stars: 18255
---

Always add appropriate safety checks before operations that could result in undefined behavior, null references, or memory issues. This includes using weak references to prevent retain cycles, verifying exact object types before type-specific operations, and adding conditional checks before calling methods that may return undefined values.

Examples of safety checks to implement:
- Use weak references for properties that could create circular dependencies: `@property (nonatomic, weak) id<YGLayoutEntity> entity;`
- Verify exact object types when behavior differs between base class and subclasses: `_isUIView = [view isMemberOfClass:[UIView class]];`
- Add conditional guards before calling methods that might not be safe for all object states: `if (!view.yoga.isUIView || [view.subviews count] > 0) { /* safe to call sizeThatFits */ }`

These patterns prevent crashes, memory leaks, and unexpected behavior by ensuring operations are only performed when it's safe to do so.