---
title: optimize with bit manipulation
description: Use bit manipulation techniques to optimize memory usage and computational
  efficiency in data structures and enums. For flag enums, consistently use bit-shift
  notation `(1 << n)` to make bit positions explicit and enable efficient bitwise
  operations. For compact data representation, leverage bitfields within unions to
  pack multiple boolean flags into...
repository: hyprwm/Hyprland
label: Algorithms
language: Other
comments_count: 3
repository_stars: 28863
---

Use bit manipulation techniques to optimize memory usage and computational efficiency in data structures and enums. For flag enums, consistently use bit-shift notation `(1 << n)` to make bit positions explicit and enable efficient bitwise operations. For compact data representation, leverage bitfields within unions to pack multiple boolean flags into minimal memory space.

Example of bit-shift enum notation:
```cpp
enum eRectCorner {
    CORNER_NONE        = 0,
    CORNER_TOPLEFT     = 1 << 0,
    CORNER_TOPRIGHT    = 1 << 1,
    CORNER_BOTTOMRIGHT = 1 << 2,
    CORNER_BOTTOMLEFT  = 1 << 3
};
```

Example of bitfield optimization:
```cpp
union {
    uint16_t all = 0;
    struct {
        bool buffer : 1;
        bool damage : 1;
        bool scale : 1;
        // ... more flags
    };
};
```

This approach reduces memory footprint, enables efficient bitwise operations for flag combinations, and leverages compiler optimizations for bit manipulation algorithms.