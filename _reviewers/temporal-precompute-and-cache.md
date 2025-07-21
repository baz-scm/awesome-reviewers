---
title: Precompute and cache
description: Avoid performing expensive operations repeatedly, especially in hot code
  paths. Identify operations such as parsing, deserialization, or configuration lookups
  that can be done once and reused.
repository: temporalio/temporal
label: Performance Optimization
language: Go
comments_count: 6
repository_stars: 14953
---

Avoid performing expensive operations repeatedly, especially in hot code paths. Identify operations such as parsing, deserialization, or configuration lookups that can be done once and reused.

Three key strategies:

1. **Move computation to initialization**:
```go
// Inefficient: Parsing on every evaluation
func (w *workerQueryEngine) EvaluateWorker(hb *workerpb.WorkerHeartbeat) (bool, error) {
    query, err := prepareQuery(w.query) // Parsing repeatedly
    // ...
}

// Optimized: Parse once during initialization
func newWorkerQueryEngine(nsID string, query string) *workerQueryEngine {
    parsedQuery, _ := prepareQuery(query) // Parse once
    return &workerQueryEngine{
        nsID:        nsID,
        query:       query,
        parsedQuery: parsedQuery,
    }
}
```

2. **Cache expensive results**:
```go
// Add a TODO for caching deserialized tasks
taskValue, err := deserializeTask(registrableTask, taskInfo.Data)
// TODO: Cache the deserialized task to avoid repeated deserialization
```

3. **Use pointers to existing data**:
```go
// Inefficient: Creates new allocation
return &cv, nil

// Efficient: Returns pointer to existing data
return &cvs[idx], nil // Returns pointer into slice, avoiding allocation
```

4. **Calculate values once and pass as parameters**:
```go
// Inefficient: Repeatedly evaluating expensive config
for _, start := range starts {
    if e.shouldYield(scheduler, *actionsTaken) { // Config lookup each time
        break
    }
    // ...
}

// Efficient: Calculate once and reuse
tweakables := e.Config.Tweakables(scheduler.Namespace)
maxActions := tweakables.MaxActionsPerExecution
for _, start := range starts {
    if *actionsTaken >= maxActions {
        break
    }
    // ...
}
```

Also consider proper ordering of operations - perform cheap checks before expensive ones. For example, check exclusion conditions before making dynamic config calls.