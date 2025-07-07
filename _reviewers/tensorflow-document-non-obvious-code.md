---
title: Document non-obvious code
description: 'Add clarifying comments to improve code readability and maintainability
  when code behavior isn''t immediately obvious. Two key practices to follow:


  1. **Label non-obvious function arguments** with the `/*arg=*/` prefix to clarify
  their purpose. This is especially important for boolean flags, magic numbers, or
  default values where the meaning isn''t...'
repository: tensorflow/tensorflow
label: Documentation
language: Other
comments_count: 2
repository_stars: 190625
---

Add clarifying comments to improve code readability and maintainability when code behavior isn't immediately obvious. Two key practices to follow:

1. **Label non-obvious function arguments** with the `/*arg=*/` prefix to clarify their purpose. This is especially important for boolean flags, magic numbers, or default values where the meaning isn't self-evident.

Example:
```cpp
// Poor: Parameters without context
rescaled_type = uint8_type.clone(buildQTypeFromMinMax(
    builder, uint8_element_quant_type.getExpressedType(),
    builder.getF64FloatAttr(type_range_min),
    builder.getF64FloatAttr(type_range_max),
    builder.getI32IntegerAttr(
        uint8_element_quant_type.getStorageTypeIntegralWidth()),
    0, true, builder.getBoolAttr(narrow_range)));

// Better: Non-obvious arguments labeled
rescaled_type = uint8_type.clone(buildQTypeFromMinMax(
    builder, uint8_element_quant_type.getExpressedType(),
    builder.getF64FloatAttr(type_range_min),
    builder.getF64FloatAttr(type_range_max),
    builder.getI32IntegerAttr(
        uint8_element_quant_type.getStorageTypeIntegralWidth()),
    /*bias=*/0, /*signed=*/true, builder.getBoolAttr(narrow_range)));
```

2. **Provide detailed comments with examples** for complex code blocks. When implementing logic that's not immediately intuitive, include examples of inputs and expected outputs or describe the transformation being performed.

For instance, when writing code that manipulates compiler include paths:
```cpp
// This fixes include paths by also including paths where resolved symlinks are replaced
// by the original paths. Example:
// If cc returns "/usr/bin/gcc/lib/include" but the actual path is a symlink from
// "/usr/lib/include", both paths will be included to ensure proper header resolution.
```

These documentation practices help other developers understand code intent without having to reverse-engineer the logic, reducing maintenance burden and preventing bugs during future modifications.