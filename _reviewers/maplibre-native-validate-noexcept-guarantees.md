---
title: Validate noexcept guarantees
description: 'Only mark functions as `noexcept` when you can guarantee they won''t
  throw exceptions under any circumstances. Common pitfalls include:


  1. **Hidden allocations**: Operations like vector operations, `std::make_tuple`,
  or working with collections might allocate memory and throw.'
repository: maplibre/maplibre-native
label: Error Handling
language: Other
comments_count: 8
repository_stars: 1411
---

Only mark functions as `noexcept` when you can guarantee they won't throw exceptions under any circumstances. Common pitfalls include:

1. **Hidden allocations**: Operations like vector operations, `std::make_tuple`, or working with collections might allocate memory and throw.
2. **Dependent types**: When using templates, the operations performed on template parameters might throw.
3. **Non-noexcept components**: If a class member or base class has non-noexcept operations, derived classes shouldn't blindly use `noexcept`.

For complex templated code, consider compile-time validation:

```cpp
// Before marking a templated function as noexcept
template <typename DataDrivenPaintProperty, typename Evaluated>
static bool isConstant(const Evaluated& evaluated) noexcept {
    // How do you know all operations here are truly noexcept?
    return evaluated.template get<DataDrivenPaintProperty>().isConstant();
}

// Better: Add compile-time verification
template <typename DataDrivenPaintProperty, typename Evaluated>
static bool isConstant(const Evaluated& evaluated) noexcept {
    using ReturnType = decltype(evaluated.template get<DataDrivenPaintProperty>());
    static_assert(std::is_nothrow_invocable_v<decltype(&ReturnType::isConstant), ReturnType&>,
                  "isConstant() must be noexcept");
    return evaluated.template get<DataDrivenPaintProperty>().isConstant();
}
```

When in doubt, err on the side of caution and omit `noexcept`. Incorrect `noexcept` specifications can lead to program termination if an exception is thrown, which is worse than having a potentially throwing function not marked as `noexcept`.