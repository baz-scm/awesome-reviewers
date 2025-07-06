---
title: Abstract model operations cleanly
description: 'When implementing AI model operations, create clean abstractions through
  interfaces that separate core mathematical operations from specific implementations.
  This enables:'
repository: ollama/ollama
label: AI
language: Go
comments_count: 5
repository_stars: 145704
---

When implementing AI model operations, create clean abstractions through interfaces that separate core mathematical operations from specific implementations. This enables:
- Swapping in optimized implementations
- Clear error handling boundaries
- Documentation of mathematical operations
- Easier testing and maintenance

Example:
```go
// Define interface for core operation
type ScaledDotProductAttention interface {
    // Document mathematical operation
    // Attention(Q,K,V) = softmax(QK^T/√d_k)V
    Forward(ctx Context, key, value, mask Tensor, scale float64) Tensor
}

// Implementation with proper validation and documentation
func Attention(ctx Context, query, key, value, mask Tensor, scale float64) Tensor {
    // Validate shapes match
    if !ValidateShapes(query, key, value, mask) {
        return nil, fmt.Errorf("invalid tensor shapes for attention")
    }
    
    // Use optimized implementation if available
    if sdpa, ok := query.(ScaledDotProductAttention); ok {
        return sdpa.Forward(ctx, key, value, mask, scale)
    }
    
    // Fallback to manual implementation
    kq := key.MulmatFullPrec(ctx, query)
    kq = kq.Scale(ctx, scale)
    kq = kq.Add(ctx, mask)
    return kq.Softmax(ctx)
}
```