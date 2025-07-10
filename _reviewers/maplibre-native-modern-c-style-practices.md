---
title: Modern C++ style practices
description: 'Apply modern C++ features and consistent syntax patterns to improve
  code readability and safety. Follow these guidelines:


  1. Use modern C++ features:'
repository: maplibre/maplibre-native
label: Code Style
language: C++
comments_count: 7
repository_stars: 1411
---

Apply modern C++ features and consistent syntax patterns to improve code readability and safety. Follow these guidelines:

1. Use modern C++ features:
- Prefer structured bindings for tuple unpacking:
```cpp
// Instead of:
for (const auto& tuple : glyphsToUpload) {
    const auto& texHandle = std::get<0>(tuple);
    const auto& glyph = std::get<1>(tuple);
}

// Use:
for (auto [texHandle, glyph, fontStack] : glyphsToUpload) {
    // ...
}
```

2. Use safe casting practices:
- Prefer static_cast over C-style casts:
```cpp
// Instead of:
auto i = (mbgl::style::PluginLayer::Impl*)baseImpl.get();

// Use:
auto i = static_cast<mbgl::style::PluginLayer::Impl*>(baseImpl.get());
```

3. Maintain consistent syntax:
- Always use braces for multi-line conditionals
- Always initialize variables, even if immediately set
- Use default comparison operators where possible in C++20:
```cpp
// Instead of:
bool operator==(const TileEntry& other) const noexcept {
    return id == other.id && sourceID == other.sourceID && op == other.op;
}

// Use:
bool operator==(const TileEntry& other) const = default;
```

These practices improve code safety, readability, and maintainability while leveraging modern C++ features.