---
title: implement or fail explicitly
description: Algorithmic functions should either correctly implement their intended
  behavior or explicitly fail with an error, rather than silently returning potentially
  incorrect or unchanged results. This prevents subtle bugs where callers assume the
  algorithm was applied when it wasn't.
repository: ggml-org/llama.cpp
label: Algorithms
language: Python
comments_count: 2
repository_stars: 83559
---

Algorithmic functions should either correctly implement their intended behavior or explicitly fail with an error, rather than silently returning potentially incorrect or unchanged results. This prevents subtle bugs where callers assume the algorithm was applied when it wasn't.

When implementing algorithmic functions, avoid "do nothing" fallback behavior that could mask errors. Instead, either:
1. Implement the complete algorithm for all supported input types
2. Throw an explicit error for unsupported cases

For example, in a quantization function:

```python
def quantize(data: np.ndarray, qtype: GGMLQuantizationType) -> np.ndarray:
    if qtype == GGMLQuantizationType.F32:
        return data.astype(np.float32, copy=False)
    elif qtype == GGMLQuantizationType.F16:
        return data.astype(np.float16, copy=False)
    elif (q := _type_traits.get(qtype)) is not None:
        return q.quantize(data)
    # BAD: Silent no-op that defeats the function's purpose
    # elif is_tmac_dtype(qtype):
    #     return data
    # GOOD: Explicit error for unsupported types
    else:
        raise QuantError(f"Quantization not implemented for type {qtype}")
```

This principle also applies to detection algorithms - they should clearly indicate when they cannot provide meaningful results rather than producing potentially misleading output.