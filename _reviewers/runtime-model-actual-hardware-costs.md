---
title: Model actual hardware costs
description: Base optimization decisions on accurate hardware cost models rather than
  outdated assumptions. Modern architectures have different performance characteristics
  for operations than older hardware, especially for SIMD and memory operations.
repository: dotnet/runtime
label: Performance Optimization
language: C++
comments_count: 6
repository_stars: 16578
---

Base optimization decisions on accurate hardware cost models rather than outdated assumptions. Modern architectures have different performance characteristics for operations than older hardware, especially for SIMD and memory operations.

When modeling operation costs:
1. Use realistic encoding and execution cycle estimates for different instruction types
2. Consider alignment requirements that balance performance with code size
3. Account for specialized hardware features like SIMD register volatility

For example, instead of using simplified cost models:

```csharp
// Outdated cost model assumes all floating point operations are expensive
if (varTypeIsFloating(candidate->Expr()->TypeGet()))
{
    // floating point loads/store encode larger
    cse_def_cost += 2;
    cse_use_cost += 1;
}
```

Consider the actual hardware characteristics:

```csharp
// Accurate cost model based on instruction encoding and execution cycles
if (varTypeIsFloating(candidate->Expr()->TypeGet()))
{
    // 32/64-bit FP move: encoding 4 bytes; execution: 4-7 cycles
    cse_def_cost += 4;
    cse_use_cost += 2;
}
else if (candidate->Expr()->TypeIs(TYP_SIMD16))
{
    // 128-bit SIMD move: encoding 3-4 bytes; execution: 4-7 cycles
    cse_def_cost += 3;
    cse_use_cost += 2;
}
else if (candidate->Expr()->TypeIs(TYP_SIMD32))
{
    // 256-bit SIMD move: encoding 4-5 bytes; execution: 5-8 cycles
    cse_def_cost += 4;
    cse_use_cost += 3;
}
```

For alignment decisions, consider both performance and code size goals:

```csharp
// Balance alignment with code size goals
UNATIVE_OFFSET cnsSize  = genTypeSize(targetType);
UNATIVE_OFFSET cnsAlign = (compiler->compCodeOpt() != Compiler::SMALL_CODE) ? cnsSize : 1;
```

When optimization decisions depend on hardware-specific behavior (like SIMD register spilling), document the rationale to prevent future regressions.
