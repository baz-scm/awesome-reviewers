---
title: Configuration over hardcoding
description: When designing APIs, prefer exposing behavior through configuration options
  rather than hardcoding logic, especially for aspects that might vary across implementations
  or require customization. This creates more flexible APIs that can adapt to changing
  requirements without code modifications.
repository: maplibre/maplibre-native
label: API
language: C++
comments_count: 2
repository_stars: 1411
---

When designing APIs, prefer exposing behavior through configuration options rather than hardcoding logic, especially for aspects that might vary across implementations or require customization. This creates more flexible APIs that can adapt to changing requirements without code modifications.

For example, instead of hardcoding mappings between Unicode ranges and font files:

```json
// Hardcoded approach requiring code changes for new languages
if (isInDevanagari(ch)) return GlyphIDType::Devanagari;
if (isInKhmer(ch)) return GlyphIDType::Khmer;
```

Design a configuration-driven approach:
```json
// Configuration-driven approach
"fonts": [
  {
    "name": "devanagari",
    "url": "https://example.com/devanagari.ttf",
    "unicode-range": "U+0900-097F"
  },
  {
    "name": "khmer",
    "url": "https://example.com/khmer.ttf",
    "unicode-range": "U+1780-17FF"
  }
]
```

This pattern applies to many API aspects like URI scheme handling, internationalization support, and feature flags. Configuration-driven APIs are more adaptable, easier to extend, and give API consumers more control without requiring changes to the underlying implementation.