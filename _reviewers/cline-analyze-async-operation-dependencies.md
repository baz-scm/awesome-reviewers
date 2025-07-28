---
title: Analyze async operation dependencies
description: Before choosing between sequential awaits and parallel execution (Promise.all),
  carefully analyze whether operations have dependencies that require specific execution
  order. Operations that depend on each other's results or shared state must be executed
  sequentially to prevent race conditions.
repository: cline/cline
label: Concurrency
language: TSX
comments_count: 2
repository_stars: 48299
---

Before choosing between sequential awaits and parallel execution (Promise.all), carefully analyze whether operations have dependencies that require specific execution order. Operations that depend on each other's results or shared state must be executed sequentially to prevent race conditions.

When operations must complete in a specific order (e.g., setting backend context before fetching data), use sequential awaits:

```javascript
// Sequential - when second operation depends on first
await AccountServiceClient.setUserOrganization({ organizationId })
await fetchCreditBalance() // Needs correct backend context from above
```

When operations are independent and can run concurrently, use Promise.all for better performance:

```javascript
// Parallel - when operations are independent
await Promise.all([getUserCredits(), getUserOrganizations()])
```

The key is understanding the data flow and dependencies between async operations. Don't optimize for speed at the expense of correctness - a race condition where "the subsequent call might execute with the wrong backend context" can cause subtle bugs that are difficult to debug.