---
title: Prefer values over pointers
description: When designing classes and interfaces, prefer passing lightweight objects
  by value rather than using raw pointers or converting smart pointers to raw pointers
  using `.get()`. This eliminates the risk of null dereferences and dangling pointer
  issues.
repository: maplibre/maplibre-native
label: Null Handling
language: Other
comments_count: 3
repository_stars: 1411
---

When designing classes and interfaces, prefer passing lightweight objects by value rather than using raw pointers or converting smart pointers to raw pointers using `.get()`. This eliminates the risk of null dereferences and dangling pointer issues.

For example, instead of:

```cpp
// Risky approach with raw pointers
class Parser {
public:
    std::string spriteURL;
    std::vector<std::unique_ptr<Sprite>> sprites;
    
    Sprite* getSprite() {
        return sprites[0].get();  // Dangerous: consumer could hold onto this raw pointer
    }
};
```

Prefer value semantics:

```cpp
// Safer approach with value objects
class Parser {
public:
    std::string spriteURL;
    std::vector<Sprite> sprites;  // Store as values
    
    const Sprite& getSprite() {   // Return reference with clear lifetime
        return sprites[0];
    }
    
    // Or return by value if the object is lightweight
    Sprite getSpriteCopy() {
        return sprites[0];
    }
};
```

When values aren't suitable (e.g., for polymorphic types), use smart pointers consistently throughout the API rather than mixing smart and raw pointers. This approach prevents null reference exceptions and makes ownership semantics clearer in your codebase.