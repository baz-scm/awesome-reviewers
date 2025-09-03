---
title: Validate parameter boundaries
description: Always validate that parameters contain expected types and values within
  safe boundaries, not just null/undefined checks. Optional parameters can receive
  unexpected types (like event objects), and numeric parameters need boundary validation
  to prevent invalid operations.
repository: ChatGPTNextWeb/NextChat
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 85721
---

Always validate that parameters contain expected types and values within safe boundaries, not just null/undefined checks. Optional parameters can receive unexpected types (like event objects), and numeric parameters need boundary validation to prevent invalid operations.

For optional parameters, verify the actual type matches expectations:
```js
// Bad: assumes i is either number or undefined
deleteSession(i?: number) {
  const index = i ?? get().currentSessionIndex; // fails when i is an event object
}

// Good: validate the parameter type
deleteSession(i?: number) {
  const index = (typeof i === 'number') ? i : get().currentSessionIndex;
}
```

For numeric operations, use boundary checks to prevent invalid results:
```js
// Bad: can create negative indices when historyMessageCount is 0
session.messages.slice(n - config.historyMessageCount)

// Good: ensure non-negative starting index
session.messages.slice(Math.max(0, n - config.historyMessageCount))
```

This prevents runtime errors from undefined values and invalid array operations.