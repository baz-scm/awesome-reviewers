---
title: Buffer bounds validation
description: Always validate buffer boundaries before performing memory operations
  to prevent buffer overflow vulnerabilities. When copying data into a buffer at a
  specified offset, verify that the combination of size and offset doesn't exceed
  the buffer's allocated capacity.
repository: maplibre/maplibre-native
label: Security
language: C++
comments_count: 1
repository_stars: 1411
---

Always validate buffer boundaries before performing memory operations to prevent buffer overflow vulnerabilities. When copying data into a buffer at a specified offset, verify that the combination of size and offset doesn't exceed the buffer's allocated capacity.

Example implementation for the update method:
```cpp
void BufferResource::update(const void* data, std::size_t size, std::size_t offset) {
    if (buffer && data) {
        // Security check to prevent buffer overflow
        if (size + offset > buffer->length()) {
            // Handle error appropriately: log, throw exception, or return error code
            return; // Abort operation
        }
        
        if (void* content = buffer->contents()) {
            std::memcpy(static_cast<uint8_t*>(content) + offset, data, size);
        }
    }
}
```

This validation is crucial for preventing memory corruption, application crashes, and potential security exploits that could lead to arbitrary code execution. Never trust input parameters without validation, even when they come from internal code.