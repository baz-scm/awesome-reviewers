---
title: Specify algorithmic scope precisely
description: When documenting changes to algorithms, data structures, or computational
  approaches, explicitly identify the specific components affected rather than using
  vague or generic descriptions. This includes naming exact data structure classes,
  clarifying the scope and limitations of algorithmic improvements, and using precise
  technical terminology.
repository: astral-sh/ty
label: Algorithms
language: Markdown
comments_count: 6
repository_stars: 11919
---

When documenting changes to algorithms, data structures, or computational approaches, explicitly identify the specific components affected rather than using vague or generic descriptions. This includes naming exact data structure classes, clarifying the scope and limitations of algorithmic improvements, and using precise technical terminology.

For example, instead of writing "improve subscript narrowing for safe mutable classes", specify the exact classes: "improve subscript narrowing for `collections.ChainMap`, `collections.Counter`, `collections.deque` and `collections.OrderedDict`". Similarly, when describing algorithmic support, clarify what is and isn't included - such as noting that recursive type alias support is limited to "non-generic recursive type aliases that use the `type` statement" rather than implying full recursive type support.

This precision helps developers understand exactly which algorithms and data structures are affected, prevents misconceptions about capabilities, and enables more targeted testing and usage of the improvements.