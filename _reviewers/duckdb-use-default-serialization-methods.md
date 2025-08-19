---
title: use default serialization methods
description: When adding new properties to serialization methods, use `WritePropertyWithDefault`
  and `ReadPropertyWithDefault` instead of `WriteProperty` and `ReadProperty` to maintain
  backwards compatibility. This ensures that older versions can still deserialize
  data written by newer versions by providing sensible defaults for missing properties.
repository: duckdb/duckdb
label: Migrations
language: C++
comments_count: 3
repository_stars: 32061
---

When adding new properties to serialization methods, use `WritePropertyWithDefault` and `ReadPropertyWithDefault` instead of `WriteProperty` and `ReadProperty` to maintain backwards compatibility. This ensures that older versions can still deserialize data written by newer versions by providing sensible defaults for missing properties.

Without default methods, adding new serialized properties breaks backwards compatibility because older versions cannot handle the new data format. Using default methods allows graceful degradation where older versions use default values for properties they don't understand.

Example:
```cpp
// Bad - breaks backwards compatibility
serializer.WriteProperty(212, "extra_info", extra_info);

// Good - maintains backwards compatibility  
serializer.WritePropertyWithDefault(212, "extra_info", extra_info);
```

Additionally, be cautious with `ShouldSerialize()` checks that might cause information loss when serializing to older storage versions. If critical data would be lost, prefer throwing an error on deserialization rather than silently dropping information.