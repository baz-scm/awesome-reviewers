---
title: avoid global state
description: Avoid global state in concurrent environments where multiple instances,
  workers, or clients may share the same JavaScript context. Global variables and
  singletons can lead to unpredictable behavior when accessed concurrently.
repository: rocicorp/mono
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 2091
---

Avoid global state in concurrent environments where multiple instances, workers, or clients may share the same JavaScript context. Global variables and singletons can lead to unpredictable behavior when accessed concurrently.

Instead, ensure proper ownership by making state local to specific classes or function scopes. Each instance should own its resources rather than sharing global state.

**Problematic pattern:**
```ts
// Global state shared across instances
const rwLocks = new Map<string, RWLock>();
export const ClientMetrics = {
  timeToConnect: new Gauge(),
  // ... other metrics
};
```

**Better approach:**
```ts
// Each instance owns its state
class SQLiteStore {
  private rwLock = new RWLock();
  // ...
}

class ReflectClient {
  private metrics = {
    timeToConnect: new Gauge(),
    // ... other metrics  
  };
  // ...
}
```

This prevents issues where "multiple Reflect clients running in a page at the same time... will share these constants leading to wackiness" and ensures that "everything has to be properly owned by one of the durable object classes, or local state owned by the worker fetch function."