---
title: Version APIs with care
description: 'When introducing new API features or changes, implement proper versioning
  to maintain stability and backward compatibility. Key practices:


  1. Guard experimental features behind version flags'
repository: nodejs/node
label: API
language: Other
comments_count: 7
repository_stars: 112178
---

When introducing new API features or changes, implement proper versioning to maintain stability and backward compatibility. Key practices:

1. Guard experimental features behind version flags
2. Add new enum values only at the end of existing enums
3. Maintain explicit version checks in implementation
4. Document version dependencies clearly

Example:
```cpp
// Good: New enum value added at end with experimental guard
typedef enum {
  napi_uint32_array,
  napi_float32_array,
  napi_float64_array,
#ifdef NAPI_EXPERIMENTAL
  napi_float16_array,  // New experimental feature
#endif
} napi_typedarray_type;

// Good: Implementation with version check
if (env->module_api_version != NAPI_VERSION_EXPERIMENTAL) {
  // Handle non-experimental version appropriately
}
```

This approach ensures API stability, enables proper testing between versions, and provides clear migration paths for API consumers.