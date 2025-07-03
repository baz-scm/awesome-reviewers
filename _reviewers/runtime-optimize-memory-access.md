---
title: Optimize memory access
description: When implementing performance-critical algorithms, carefully consider
  memory access patterns. Document alignment assumptions when using low-level operations
  like `MemoryMarshal.Cast` or SIMD intrinsics. Prefer reference-based APIs over pinning
  to avoid GC interference. For bulk operations, use specialized helpers like `LoadUnsafe(ref
  T source, nuint...
repository: dotnet/runtime
label: Algorithms
language: C#
comments_count: 9
repository_stars: 16578
---

When implementing performance-critical algorithms, carefully consider memory access patterns. Document alignment assumptions when using low-level operations like `MemoryMarshal.Cast` or SIMD intrinsics. Prefer reference-based APIs over pinning to avoid GC interference. For bulk operations, use specialized helpers like `LoadUnsafe(ref T source, nuint elementOffset)` instead of pointer arithmetic.

```csharp
// Less optimal: Uses pinning that can hinder GC
unsafe void ProcessBytes(ReadOnlySpan<byte> source)
{
    fixed (byte* ptr = source)
    {
        for (int i = 0; i < source.Length - 7; i += 8)
        {
            ulong value = *(ulong*)(ptr + i);
            // Process 8 bytes at once
        }
    }
}

// More optimal: Uses ref-based API without pinning
void ProcessBytes(ReadOnlySpan<byte> source)
{
    ref byte sourceRef = ref MemoryMarshal.GetReference(source);
    for (int i = 0; i + 8 <= source.Length; i += 8)
    {
        // Use LoadUnsafe with explicit offset
        ulong value = Vector64.LoadUnsafe(ref sourceRef, (nuint)i);
        // Process 8 bytes at once
    }
}
```

When handling data in bulk, consider the impact of alignment requirements and document edge cases like zero-length inputs. For operations on numeric types, select appropriate operations based on platform characteristics (e.g., prefer unsigned division over signed when possible).
