---
title: Follow modern C++ guidelines
description: 'Adhere to the C++ Core Guidelines for improved code quality, readability,
  and maintainability. Follow these key practices:


  1. **Use enum class instead of regular enums** for type safety and scope:'
repository: maplibre/maplibre-native
label: Code Style
language: Other
comments_count: 11
repository_stars: 1411
---

Adhere to the C++ Core Guidelines for improved code quality, readability, and maintainability. Follow these key practices:

1. **Use enum class instead of regular enums** for type safety and scope:
```cpp
// Avoid
enum {
    collisionTextureCount
};

// Prefer
enum class CollisionTexture {
    Count
};
```

2. **Use `using` over `typedef`** for improved readability:
```cpp
// Avoid
typedef CollisionUBO CollisionBoxUBO;

// Prefer
using CollisionBoxUBO = CollisionUBO;
```

3. **Mark methods as const when they don't modify object state**:
```cpp
// Avoid
std::vector<std::string> getLog();

// Prefer
std::vector<std::string> getLog() const;
```

4. **Use override without redundant virtual**:
```cpp
// Avoid
virtual void setSynchronous(bool value) override { synchronousFrame = value; }

// Prefer
void setSynchronous(bool value) override { synchronousFrame = value; }
```

These practices align with modern C++ standards, reduce potential bugs, and make the code easier to understand and maintain. The C++ Core Guidelines provide comprehensive recommendations for writing clear, correct, and efficient C++ code.