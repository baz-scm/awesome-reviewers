---
title: Group related properties
description: Design APIs by organizing related properties into purpose-specific structures
  rather than flat parameter lists. This improves clarity about which properties apply
  in different contexts, enhances API documentation, and makes interfaces more maintainable
  as they evolve.
repository: maplibre/maplibre-native
label: API
language: Other
comments_count: 3
repository_stars: 1411
---

Design APIs by organizing related properties into purpose-specific structures rather than flat parameter lists. This improves clarity about which properties apply in different contexts, enhances API documentation, and makes interfaces more maintainable as they evolve.

When designing APIs that handle multiple property types or target different use cases, create specialized structures that clearly indicate their purpose. This practice:

1. Makes code more self-documenting
2. Reduces confusion about which properties are applicable in different contexts
3. Provides better organization as APIs grow
4. Simplifies future extensions

For example, instead of placing multiple property setters at the interface level:

```cpp
// Less clear approach
class Interface {
public:
    void setColor(Color color);
    void setBlur(float blur);
    void setWidth(float width);
    
    void addPolyline(/* parameters */);
    void addFill(/* parameters */);
};
```

Group related properties into purpose-specific structures:

```cpp
// Better organized approach
class Interface {
public:
    struct LineOptions {
        Color color;
        float blur;
        float width;
    };
    
    struct FillOptions {
        Color color;
        float opacity;
    };
    
    void addPolyline(const LineOptions& options, /* other parameters */);
    void addFill(const FillOptions& options, /* other parameters */);
};
```

This pattern also helps with API evolution - when adding new properties, you can clearly see which structure they belong to, and clients only need to consider properties relevant to their use case.