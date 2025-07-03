---
title: Platform-aware algorithm optimization
description: When implementing performance-critical algorithms, design your code to
  detect and utilize platform-specific hardware features while maintaining compatibility
  across different architectures. Create abstraction layers that allow the same algorithm
  to run on various platforms but take advantage of specialized instruction sets (like
  AVX extensions) when...
repository: dotnet/runtime
label: Algorithms
language: Txt
comments_count: 2
repository_stars: 16578
---

When implementing performance-critical algorithms, design your code to detect and utilize platform-specific hardware features while maintaining compatibility across different architectures. Create abstraction layers that allow the same algorithm to run on various platforms but take advantage of specialized instruction sets (like AVX extensions) when available.

For example, instead of directly using platform-specific code:

```csharp
// Not recommended - tightly coupled to specific hardware
public void ProcessData(float[] data)
{
    if (Avx2.IsSupported)
    {
        // Use AVX2 instructions
    }
    else
    {
        // Fallback implementation
    }
}
```

Create a strategy pattern that selects the appropriate implementation:

```csharp
// Recommended approach
public interface IDataProcessor
{
    void ProcessData(float[] data);
}

public class DataProcessorFactory
{
    public static IDataProcessor Create()
    {
        if (Avx2.IsSupported)
        {
            return new Avx2DataProcessor();
        }
        else if (Sse.IsSupported)
        {
            return new SseDataProcessor();
        }
        return new DefaultDataProcessor();
    }
}
```

This approach facilitates platform-specific optimizations while maintaining clean separation of concerns, makes testing easier, and allows for future extensions as new instruction sets become available.
