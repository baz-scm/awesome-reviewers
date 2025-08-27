---
title: Always check errors
description: Always check and handle errors returned from function calls, especially
  API operations, before proceeding with subsequent logic. Unchecked errors can lead
  to inconsistent state, data corruption, or unexpected behavior.
repository: volcano-sh/volcano
label: Error Handling
language: Go
comments_count: 4
repository_stars: 4899
---

Always check and handle errors returned from function calls, especially API operations, before proceeding with subsequent logic. Unchecked errors can lead to inconsistent state, data corruption, or unexpected behavior.

Key practices:
- Check errors immediately after API calls (Update, Get, Delete operations)
- Return or handle errors appropriately rather than ignoring them
- Ensure error handling occurs before updating related state or variables
- Add proper error handling even in seemingly "safe" operations

Example of missing error check:
```go
// Bad: Error not checked
_, err = vcClient.TopologyV1alpha1().HyperNodes().Update(context.Background(), current, metav1.UpdateOptions{})
// Continuing without checking err can cause issues

// Good: Error properly handled
_, err = vcClient.TopologyV1alpha1().HyperNodes().Update(context.Background(), current, metav1.UpdateOptions{})
if err != nil {
    return err
}
```

Example of proper error handling with state management:
```go
// Check error before updating state variables
if err := sc.executePreBind(ctx, bindContext); err != nil {
    // Handle error and ensure cleanup/resync occurs
    sc.resyncTask(bindContext.TaskInfo)
    return err
}
// Only proceed with state updates after successful operation
```

This practice prevents silent failures, ensures consistent error propagation, and maintains system reliability by catching issues early in the execution flow.