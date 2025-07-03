---
title: Clear API contracts
description: Design APIs with clear contracts that behave exactly as their names and
  signatures suggest. Functions should do precisely what they claim to do without
  surprising side effects or hidden behaviors.
repository: opencv/opencv
label: API
language: C++
comments_count: 6
repository_stars: 82865
---

Design APIs with clear contracts that behave exactly as their names and signatures suggest. Functions should do precisely what they claim to do without surprising side effects or hidden behaviors.

Key principles:
- Function behavior must strictly align with its name and signature
- Prefer simplified interfaces that abstract implementation details
- Be explicit about parameter requirements and behaviors
- Raise errors for invalid operations rather than using fallback paths
- Use sensible defaults that follow established conventions

**Example of poor design:**
```cpp
// Confusing API with unclear behavior
bool initializeContextFromVA(VADisplay display, bool tryInterop) {
    // Uses a different display if provided one doesn't work
    // Silently falls back to non-interop mode if tryInterop fails
    // Returns success even when not using the requested display
}
```

**Improved design:**
```cpp
// Clear contract, predictable behavior
bool initializeContextFromVA(VADisplay display) {
    // Only initializes with the exact display provided
    // Throws exception with clear message if initialization fails
    // Returns true only when successfully initialized with given display
}
```

Remember to document any special parameter handling. If your function treats certain values (like Point(0,0)) specially, make this explicit in both the function signature (with default parameters) and documentation. When extending existing APIs, maintain consistency with established patterns in the codebase.
