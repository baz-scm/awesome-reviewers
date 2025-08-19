---
title: Constructor configuration injection
description: Prefer injecting configuration objects through constructors rather than
  passing them as ad-hoc parameters or using global instances. This approach improves
  extensibility, reduces error-prone context passing, and enables per-instance customization.
repository: duckdb/duckdb
label: Configurations
language: Other
comments_count: 4
repository_stars: 32061
---

Prefer injecting configuration objects through constructors rather than passing them as ad-hoc parameters or using global instances. This approach improves extensibility, reduces error-prone context passing, and enables per-instance customization.

Instead of passing configuration parameters to individual methods or relying on global singletons, inject configuration objects during construction:

```cpp
// Avoid: Ad-hoc parameter passing
void LoadExistingDatabase(optional_ptr<string> encryption_key = nullptr);
read_head.buffer_handle = file_handle.Read(QueryContext(), read_head.buffer_ptr, read_head.size, read_head.location);

// Prefer: Constructor injection
class ThriftFileTransport {
    ClientContext &context;
public:
    ThriftFileTransport(ClientContext &ctx) : context(ctx) {}
    // Use injected context instead of creating new QueryContext()
};

class SingleFileBlockManager {
    StorageManagerOptions options;
public:
    SingleFileBlockManager(StorageManagerOptions opts) : options(opts) {}
    // Use options.encryption_key instead of method parameters
};
```

Avoid global configuration instances that prevent extension customization. Instead, store configuration in `DatabaseInstance` or `DBConfig` to support per-instance settings and extension registration.