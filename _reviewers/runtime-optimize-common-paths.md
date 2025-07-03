---
title: Optimize common paths
description: 'Design algorithms that optimize for the most common execution paths
  by prioritizing frequent scenarios in conditional logic, data structures, and resource
  allocation. '
repository: dotnet/runtime
label: Algorithms
language: Other
comments_count: 6
repository_stars: 16578
---

Design algorithms that optimize for the most common execution paths by prioritizing frequent scenarios in conditional logic, data structures, and resource allocation. 

For conditional code, order checks to minimize branching in frequent cases:

```cpp
// Better: Common case first requires only one check
if (varTypeUsesIntReg(type))
{
    return IntRegisterType;
}
// Less common case
else if (varTypeUsesMaskReg(type))
{
    return MaskRegisterType;
}
// Least common case with assertion
else
{
    assert(varTypeUsesFloatReg(type));
    return FloatRegisterType;
}
```

Pre-compute constants instead of calculating them at runtime, especially for cross-platform compatibility:

```cpp
// Better: Pre-computed value
cmp         rsi, 0x8000000 // (0x40000000 / sizeof(void*))

// Worse: Compiler-dependent calculation
cmp         rsi, (0x40000000 / 8) // sizeof(void*)
```

Focus testing and optimization efforts on the most frequently used combinations of features rather than exhaustively covering all permutations. This "pay for play" approach ensures users only bear the computational cost for features they actually use.
