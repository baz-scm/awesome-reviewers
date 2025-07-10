---
title: Externalize config values
description: Replace hardcoded "magic numbers" and environment-specific logic with
  externally configurable values. Use preprocessor definitions, build flags, or configuration
  constants to make your code adaptable to different environments and requirements.
repository: maplibre/maplibre-native
label: Configurations
language: C++
comments_count: 3
repository_stars: 1411
---

Replace hardcoded "magic numbers" and environment-specific logic with externally configurable values. Use preprocessor definitions, build flags, or configuration constants to make your code adaptable to different environments and requirements.

For numeric constants, define them as configurable parameters:
```cpp
// BAD: Hardcoded magic numbers
const std::vector<vk::DescriptorPoolSize> poolSizes = {
    {vk::DescriptorType::eUniformBuffer, 10000},
    {vk::DescriptorType::eCombinedImageSampler, 5000},
};

// GOOD: Configurable via build flags
#ifndef MLN_VULKAN_DESCRIPTOR_POOL_SIZE
#define MLN_VULKAN_DESCRIPTOR_POOL_SIZE 10000
#endif

const std::vector<vk::DescriptorPoolSize> poolSizes = {
    {vk::DescriptorType::eUniformBuffer, MLN_VULKAN_DESCRIPTOR_POOL_SIZE},
    {vk::DescriptorType::eCombinedImageSampler, MLN_VULKAN_DESCRIPTOR_POOL_SIZE/2},
};
```

For feature-specific or platform-specific code, use preprocessor conditionals:
```cpp
// Only load extensions when the related feature is enabled
#ifdef MLN_USE_TRACY
extension::loadTimeStampQueryExtension(fn);
#endif

// Handle platform-specific behavior
#if !defined(__QT__)
TEST(Image, WebPTile) {
    // Test implementation
}
#endif
```

This approach improves maintainability, makes platform-specific behavior explicit, and allows for customization without code changes.