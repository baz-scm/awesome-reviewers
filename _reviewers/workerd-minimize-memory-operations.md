---
title: minimize memory operations
description: 'Avoid unnecessary memory allocations, copies, and inefficient memory
  usage patterns that can impact performance. This includes several key practices:

  '
repository: cloudflare/workerd
label: Performance Optimization
language: Other
comments_count: 6
repository_stars: 6989
---

Avoid unnecessary memory allocations, copies, and inefficient memory usage patterns that can impact performance. This includes several key practices:

**Avoid unnecessary allocations:**
- Use static allocation instead of heap allocation when possible: `static NullIoStream globalNullStream;` instead of `static auto globalNullStream = kj::heap<NullIoStream>();`
- Avoid intermediate string copies: prefer direct construction over `kj::str(...)` when the result is immediately wrapped

**Optimize parameter passing:**
- Use const references for non-trivial types to prevent copies: `const tracing::TraceId& traceId` instead of `tracing::TraceId traceId`
- Use move semantics appropriately, but be aware that explicit `kj::mv()` can interfere with NRVO (Named Return Value Optimization)

**Pre-allocate when size is known:**
```cpp
// Instead of letting vector grow dynamically
kj::Vector<kj::Promise<void>> promises;
// Reserve space when size is known
promises.reserve(filenames.size());
```

**Choose efficient memory usage patterns:**
- Pump data to null streams instead of buffering in memory when data will be discarded: avoid `readAllBytes()` that buffers unnecessarily
- Use more efficient construction methods: `kj::Path({"tmp"})` instead of `kj::Path::parse("tmp")`

These optimizations are particularly important in hot paths or when processing large amounts of data, as small inefficiencies can compound significantly.