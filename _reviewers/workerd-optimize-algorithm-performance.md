---
title: Optimize algorithm performance
description: When implementing algorithms, prioritize performance by using batching
  techniques to reduce API call overhead and avoiding unnecessary memory allocations.
  Convert recursive algorithms to iterative ones when dealing with large datasets,
  and process elements in batches rather than individually.
repository: cloudflare/workerd
label: Algorithms
language: Other
comments_count: 2
repository_stars: 6989
---

When implementing algorithms, prioritize performance by using batching techniques to reduce API call overhead and avoiding unnecessary memory allocations. Convert recursive algorithms to iterative ones when dealing with large datasets, and process elements in batches rather than individually.

Key optimization strategies:
1. **Batch processing**: Group operations to reduce overhead from repeated API calls
2. **Avoid unnecessary allocations**: Use efficient string/memory operations (e.g., `js.str()` instead of `kj::str()`, `chars.first()` instead of `chars.slice()`)
3. **Queue management**: Pre-reserve capacity and filter out null/undefined values early

Example from recursive to iterative optimization:
```cpp
// Instead of recursive calls, use iterative approach with batching
kj::Vector<v8::Local<v8::Value>> queue;
queue.reserve(128);

while (!queue.empty()) {
    auto item = queue.back();
    queue.removeLast();
    
    if (item->IsArray()) {
        auto arr = item.As<v8::Array>();
        constexpr uint32_t BATCH_SIZE = 32;
        
        for (uint32_t i = 0; i < length;) {
            uint32_t batchEnd = kj::min(i + BATCH_SIZE, length);
            queue.reserve(queue.size() + (batchEnd - i));
            
            for (; i < batchEnd; ++i) {
                auto element = check(arr->Get(context, i));
                if (!element->IsNullOrUndefined()) {
                    queue.add(element);
                }
            }
        }
    }
}
```

This approach reduces V8 API call overhead and manages memory more efficiently than naive recursive implementations.