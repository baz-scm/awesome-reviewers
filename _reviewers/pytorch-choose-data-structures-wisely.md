---
title: Choose data structures wisely
description: When designing algorithms, select data structures that accommodate all
  possible scenarios, not just the common case. For static analysis algorithms where
  certainty isn't guaranteed, prefer collections that can represent one-to-many relationships
  even when most instances will contain only one element. This prevents having to
  redesign your algorithm later...
repository: pytorch/pytorch
label: Algorithms
language: Other
comments_count: 2
repository_stars: 91345
---

When designing algorithms, select data structures that accommodate all possible scenarios, not just the common case. For static analysis algorithms where certainty isn't guaranteed, prefer collections that can represent one-to-many relationships even when most instances will contain only one element. This prevents having to redesign your algorithm later when edge cases are discovered.

For example, instead of using:
```cpp
c10::FastMap<const Value*, const Value*> aliases_; // One-to-one mapping
```

Use a structure that supports potential multiple relationships:
```cpp
c10::FastMap<const Value*, c10::FastSet<const Value*>> aliases_; // One-to-many mapping
```

This approach is particularly important in static analysis, compiler optimizations, and other scenarios where the algorithm must account for all possible execution paths, even if most runtime instances follow a simpler pattern.