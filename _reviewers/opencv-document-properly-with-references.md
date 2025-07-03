---
title: Document properly with references
description: 'Always separate code from documentation and use proper referencing techniques.
  Documentation should be in markdown files when extensive, while code should be in
  files that are regularly checked for compilation. '
repository: opencv/opencv
label: Documentation
language: Other
comments_count: 4
repository_stars: 82865
---

Always separate code from documentation and use proper referencing techniques. Documentation should be in markdown files when extensive, while code should be in files that are regularly checked for compilation. 

When documenting APIs:
1. Use `CV_EXPORTS_W` for functions that should be included in Java and Python bindings
2. Reference existing documentation rather than duplicating descriptions
3. Use `@snippet` and `@include` directives to embed code examples in documentation
4. Ensure all parameters are fully documented

**Example - Avoid:**
```cpp
/** @brief Enum of the possible types of ccm.
*/
enum CCM_TYPE
{
    CCM_3x3,   ///< The CCM with the shape \f$3\times3\f$ performs linear transformation on color values.
    CCM_4x3,   ///< The CCM with the shape \f$4\times3\f$ performs affine transformation.
};
// [followed by 200+ lines of in-header documentation]
```

**Example - Prefer:**
```cpp
/** @brief Enum of the possible types of ccm.
 *  @see @ref ccm_documentation for detailed explanations
*/
enum CCM_TYPE
{
    CCM_3x3,   ///< The CCM with the shape \f$3\times3\f$ performs linear transformation
    CCM_4x3,   ///< The CCM with the shape \f$4\times3\f$ performs affine transformation
};
```

With detailed documentation in a markdown file referenced by `@ref ccm_documentation` and any code examples included via `@snippet` or `@include` directives.
