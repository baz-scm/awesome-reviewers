---
title: Optimize computational complexity
description: Always analyze the computational complexity of algorithms and choose
  efficient implementations to avoid performance bottlenecks and security vulnerabilities.
  Pay special attention to avoiding O(N²) algorithms that can create DoS risks, eliminate
  unnecessary computational overhead, and select appropriate data structures.
repository: gravitational/teleport
label: Algorithms
language: Go
comments_count: 4
repository_stars: 19109
---

Always analyze the computational complexity of algorithms and choose efficient implementations to avoid performance bottlenecks and security vulnerabilities. Pay special attention to avoiding O(N²) algorithms that can create DoS risks, eliminate unnecessary computational overhead, and select appropriate data structures.

Key practices:
- Replace O(N²) nested loops with O(N) map-based lookups when possible
- Avoid unnecessary operations like roundtrip conversions that add overhead
- Choose direct implementations over marshal/unmarshal cycles when performance matters
- Reorder conditional checks to evaluate most likely conditions first

Example of problematic O(N²) code:
```go
// Avoid: O(N²) complexity with DoS risk
for _, v := range bval {
    if !slices.Contains(aval, v) {
        return false
    }
}

// Prefer: O(N) complexity using map lookup
aMap := make(map[string]bool, len(aval))
for _, v := range aval {
    aMap[v] = true
}
for _, v := range bval {
    if !aMap[v] {
        return false
    }
}
```

Consider the security implications of algorithmic complexity, especially in user-facing APIs where input size may be controlled by attackers. When dealing with large datasets or user-controlled input, always prefer linear or logarithmic algorithms over quadratic ones.