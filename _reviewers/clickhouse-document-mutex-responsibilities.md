---
title: Document mutex responsibilities
description: Use Thread Safety Analysis (TSA) annotations to explicitly document which
  mutexes protect which variables, making thread safety relationships clear to both
  static analyzers and code readers.
repository: ClickHouse/ClickHouse
label: Concurrency
language: Other
comments_count: 3
repository_stars: 42425
---

Use Thread Safety Analysis (TSA) annotations to explicitly document which mutexes protect which variables, making thread safety relationships clear to both static analyzers and code readers.

Every mutex should have a clear, documented purpose with TSA annotations that specify what data it protects. This prevents issues like unused mutexes, inconsistent locking patterns, and unclear concurrent access semantics.

Example using TSA annotations:
```cpp
class XRayInstrumentationManager {
private:
    mutable std::mutex functions_mutex;
    std::list<InstrumentedFunctionInfo> instrumented_functions GUARDED_BY(functions_mutex);
    
    InstrumentedFunctions getInstrumentedFunctions() const REQUIRES(functions_mutex) {
        std::lock_guard lock(functions_mutex);
        return instrumented_functions;
    }
};
```

For read-only concurrent access, use const-correctness and shared locks with clear documentation:
```cpp
// Functions can access this info in parallel for reading purposes only
std::pair<const IndexContextInfoPtr, std::shared_lock<std::shared_mutex>> getIndexInfo() const;
```

TSA macros like `GUARDED_BY`, `REQUIRES`, and `EXCLUDES` help catch threading issues early and make code self-documenting about its concurrency assumptions.