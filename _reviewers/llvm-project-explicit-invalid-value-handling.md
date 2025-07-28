---
title: explicit invalid value handling
description: When designing enums or working with type casting, explicitly define
  and handle invalid states rather than relying on undefined behavior. Use designated
  invalid values that stand out clearly, and employ equality assertions for type compatibility
  checks.
repository: llvm/llvm-project
label: Null Handling
language: Other
comments_count: 2
repository_stars: 33702
---

When designing enums or working with type casting, explicitly define and handle invalid states rather than relying on undefined behavior. Use designated invalid values that stand out clearly, and employ equality assertions for type compatibility checks.

For enums, avoid gaps in value sequences and use distinctive invalid values:
```cpp
// Instead of skipping values:
enum WasmAddressType { Memory = 0x00, Object = 0x01, Invalid = 0x03 };

// Use clear, distinctive invalid values:
enum WasmAddressType { Memory = 0x00, Object = 0x01, Invalid = 0xff };
```

For type casting scenarios, use equality assertions when types must be compatible:
```cpp
// Instead of just checking size compatibility:
static_assert(sizeof(Barrier) <= sizeof(pthread_barrier_t));

// Assert exact equality when casting between types:
static_assert(sizeof(Barrier) == sizeof(pthread_barrier_t));
```

This approach prevents undefined behavior, makes invalid states explicit and detectable, and ensures type safety through clear assertions rather than implicit assumptions.