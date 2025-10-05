---
title: Explicit value specifications
description: Always use explicit value specifications and type-safe handling to prevent
  undefined behavior and ensure predictable code execution. This includes specifying
  appropriate default values for configuration parameters and using platform-independent
  format specifiers for data types.
repository: commaai/openpilot
label: Null Handling
language: Other
comments_count: 2
repository_stars: 58214
---

Always use explicit value specifications and type-safe handling to prevent undefined behavior and ensure predictable code execution. This includes specifying appropriate default values for configuration parameters and using platform-independent format specifiers for data types.

For configuration defaults, be explicit about expected values even when they seem obvious:
```cpp
// Good: Explicit defaults prevent undefined states
{"UptimeOffroad", {PERSISTENT, FLOAT, "0.0"}},
{"UptimeOnroad", {PERSISTENT, FLOAT, "0.0"}},
```

For type formatting, use portable macros to ensure correct behavior across platforms:
```cpp
// Good: Type-safe formatting prevents undefined behavior
LOGE("SV_ID != SLOT_NUMBER: %d %" PRIu64, msg->sv_id(), data->n());

// Alternative: Explicit casting for clarity
LOGE("SV_ID != SLOT_NUMBER: %d %llu", msg->sv_id(), (unsigned long long)data->n());
```

This approach prevents subtle bugs from implicit assumptions about default values or platform-specific type representations, ensuring consistent behavior across different environments and reducing the risk of undefined states.