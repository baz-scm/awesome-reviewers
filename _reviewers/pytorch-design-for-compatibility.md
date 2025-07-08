---
title: Design for compatibility
description: 'When evolving APIs, prioritize backward compatibility to minimize disruption
  for existing users. Add new functionality using default arguments rather than creating
  overloaded methods that could cause ABI compatibility issues. For example:'
repository: pytorch/pytorch
label: API
language: C++
comments_count: 4
repository_stars: 91345
---

When evolving APIs, prioritize backward compatibility to minimize disruption for existing users. Add new functionality using default arguments rather than creating overloaded methods that could cause ABI compatibility issues. For example:

```cpp
// Prefer this:
void set_device(DeviceIndex device, bool force = false);

// Over this:
void set_device(DeviceIndex device);
void set_device(DeviceIndex device, bool force);
```

When introducing version-dependent features, implement appropriate version checks and fallbacks:

```cpp
#if defined(CUDA_VERSION) && (CUDA_VERSION >= 12050)
  // Use newer API version
#else
  // Fallback implementation for older versions
#endif
```

Keep internal implementation details hidden from public-facing interfaces by clearly distinguishing between public APIs and internal functionality. For evolving ABIs, provide transition mechanisms that support both old and new versions simultaneously, allowing consumers to opt into newer versions explicitly while maintaining backward compatibility.