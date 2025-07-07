---
title: Select algorithms by complexity
description: Choose appropriate algorithms based on computational complexity requirements
  and context. When implementing lookups, prefer O(1) direct access over O(n) iterations
  whenever possible. For infrequent operations or small datasets, simpler linear algorithms
  may outperform more complex logarithmic approaches due to lower constant factors
  and better locality.
repository: gin-gonic/gin
label: Algorithms
language: Go
comments_count: 2
repository_stars: 83022
---

Choose appropriate algorithms based on computational complexity requirements and context. When implementing lookups, prefer O(1) direct access over O(n) iterations whenever possible. For infrequent operations or small datasets, simpler linear algorithms may outperform more complex logarithmic approaches due to lower constant factors and better locality.

**Example 1:** Use direct map lookups instead of iterating over map keys:
```go
// Inefficient: O(n) iteration
for bind, fn := range negotiationRenderMappings {
    if bind == accepted {
        fn(code, config, c)
        return
    }
}

// Better: O(1) direct lookup
if fn, ok := negotiationRenderMappings[accepted]; ok {
    fn(code, config, c)
    return
}
```

**Example 2:** Choose simpler algorithms when appropriate:
```go
// Overcomplicated: Sort + binary search for simple matching
sort.Strings(extensionsAllowed)
// ...
indexFound := sort.SearchStrings(extensionsAllowed, extension)
if indexFound < len(extensionsAllowed) && extensionsAllowed[indexFound] == extension {
    // ...
}

// Better for small sets: Simple iteration
for _, v := range extensionsAllowed {
    if strings.ToLower(v) == extension {
        files = append(files, path)
    }
}
```