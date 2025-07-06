---
title: Reuse buffers strategically
description: For frequently called methods or hot code paths, reuse allocations instead
  of creating new buffers on each call. This significantly reduces GC pressure and
  improves performance in memory-intensive operations.
repository: ollama/ollama
label: Performance Optimization
language: Go
comments_count: 4
repository_stars: 145704
---

For frequently called methods or hot code paths, reuse allocations instead of creating new buffers on each call. This significantly reduces GC pressure and improves performance in memory-intensive operations.

To implement this pattern:

1. Add reusable buffer fields to structs that handle data processing
2. Check the capacity of existing buffers before allocating new ones
3. Resize only when necessary based on input requirements

Example implementation:

```go
// Before: Allocating a new buffer on each call
func (s *weighted) Sample(logits []float32) (int32, error) {
    tokens := make([]tokenInfo, len(logits))
    // Process logits...
}

// After: Reusing a buffer across calls
type weighted struct {
    rng        *rand.Rand
    transforms []transform
    buf        []tokenInfo // reusable buffer field
}

func (s *weighted) Sample(logits []float32) (int32, error) {
    // Resize only when necessary
    if cap(s.buf) < len(logits) {
        s.buf = make([]tokenInfo, len(logits))
    }
    tokens := s.buf[:len(logits)]
    // Process logits...
}
```

This pattern is especially important for functions in critical processing paths like sampling, data copying, or quantization operations. For data copying operations that don't require transformation, consider using io.Copy or similar approaches that avoid loading everything into memory.