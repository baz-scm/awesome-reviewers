---
title: Minimize reference counting overhead
description: Avoid unnecessary reference counting operations that can impact performance,
  especially in frequently called code paths. Use move semantics, appropriate pointer
  types, and efficient parameter passing to reduce AddRef/Release churn.
repository: microsoft/terminal
label: Performance Optimization
language: Other
comments_count: 4
repository_stars: 99242
---

Avoid unnecessary reference counting operations that can impact performance, especially in frequently called code paths. Use move semantics, appropriate pointer types, and efficient parameter passing to reduce AddRef/Release churn.

Key strategies:
1. **Use raw pointers when lifetime is guaranteed**: Replace `std::shared_ptr` with raw pointers when the object lifetime is managed by a parent that outlives the consumer
2. **Prefer move semantics for WinRT types**: Take WinRT parameters by value and use `std::move` when assigning to members to avoid extra AddRef/Release cycles
3. **Avoid expensive WinRT collections**: Use standard containers like `std::vector` internally and wrap with `winrt::multi_threaded_vector` only when needed for WinRT interfaces

Example transformations:
```cpp
// Before: Unnecessary shared_ptr overhead
void Constructor(const std::shared_ptr<Cache>& cache) : _cache(cache) {}

// After: Raw pointer when lifetime is guaranteed
void Constructor(Cache* cache) : _cache(cache) {}

// Before: Extra AddRef/Release on assignment  
Constructor(const IVector<T>& items) : _items(items) {}

// After: Move to avoid reference count churn
Constructor(IVector<T> items) : _items(std::move(items)) {}
```

This optimization is particularly important for frequently instantiated objects and hot code paths where reference counting overhead can accumulate significantly.