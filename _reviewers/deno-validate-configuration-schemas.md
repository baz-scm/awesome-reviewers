---
title: validate configuration schemas
description: Configuration schemas should be actively validated, well-documented,
  and kept up-to-date through automated testing. Use appropriate schema types (enums
  vs strings) based on whether values are constrained, provide comprehensive descriptions
  that include examples and supported formats, and implement automated tests to ensure
  schemas remain current with code...
repository: denoland/deno
label: Configurations
language: Json
comments_count: 2
repository_stars: 103714
---

Configuration schemas should be actively validated, well-documented, and kept up-to-date through automated testing. Use appropriate schema types (enums vs strings) based on whether values are constrained, provide comprehensive descriptions that include examples and supported formats, and implement automated tests to ensure schemas remain current with code changes.

For example, instead of a generic string type:
```json
"items": {
  "type": "string"
}
```

Use descriptive schemas with proper validation:
```json
"plugins": {
  "type": "array", 
  "description": "UNSTABLE: List of plugins to load. These can be paths, npm or jsr specifiers",
  "items": {
    "oneOf": [
      {"type": "string", "format": "uri"},
      {"enum": ["known-plugin-1", "known-plugin-2"]}
    ]
  }
}
```

Add automated tests that verify schema accuracy against actual implementation to prevent drift between documentation and behavior.