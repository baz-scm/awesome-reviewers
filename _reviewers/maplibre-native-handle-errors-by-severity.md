---
title: Handle errors by severity
description: 'Choose error handling mechanisms based on error severity and recoverability:


  1. Use throws for unrecoverable errors that prevent system operation:

  ```cpp'
repository: maplibre/maplibre-native
label: Error Handling
language: C++
comments_count: 6
repository_stars: 1411
---

Choose error handling mechanisms based on error severity and recoverability:

1. Use throws for unrecoverable errors that prevent system operation:
```cpp
VkResult result = vmaCreateAllocator(&allocatorCreateInfo, &allocator);
if (result != VK_SUCCESS) {
    throw std::runtime_error("Vulkan allocator init failed");
}
```

2. Use callbacks/return values for recoverable errors:
```cpp
HeadlessFrontend::RenderResult render(Map& map, std::exception_ptr *error) {
    map.renderStill([&](const std::exception_ptr& e) {
        if (e) { *error = e; }
    });
}
```

3. Use assertions only for developer-time invariant checking, not for runtime error handling.

Critical errors that prevent system operation should throw exceptions. Recoverable errors should be propagated via return values or callbacks to allow graceful handling. Assertions should only validate development-time invariants and not be used for runtime error handling since they're removed in release builds.