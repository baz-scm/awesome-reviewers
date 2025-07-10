---
title: Template instantiation trade-offs
description: 'When designing algorithms that accept callbacks or function parameters,
  consider the trade-off between template functions and `std::function`:


  1. **Templates generate code** - Each unique lambda passed to a template function
  creates a new instance of that entire function body, which can significantly increase
  binary size for large functions.'
repository: maplibre/maplibre-native
label: Algorithms
language: Other
comments_count: 3
repository_stars: 1411
---

When designing algorithms that accept callbacks or function parameters, consider the trade-off between template functions and `std::function`:

1. **Templates generate code** - Each unique lambda passed to a template function creates a new instance of that entire function body, which can significantly increase binary size for large functions.

2. **Use `std::function` for large function bodies** - When a function body is substantial (like in polyline generation), the code duplication cost from templates outweighs the indirection cost of `std::function`.

```cpp
// Prefer std::function for large function bodies with multiple callers
std::size_t visitDrawables(const std::function<void(gfx::Drawable&)>& f) {
    for (const auto& item : drawables) {
        if (item) {
            f(*item);
        }
    }
    return drawables.size();
}

// Templates are appropriate for small, performance-critical code
template <typename Hasher>
size_t computeHash(const T& value) {
    return Hasher{}(value);
}
```

3. **Extract complex operations** - For operations like hash combining, extract the logic to a shared function rather than duplicating it across template instantiations.

4. **Consider compile time** - Templates increase compile time, especially for complex algorithms, which can slow down the development cycle.