---
title: Ensure informative log messages
description: Log messages should be clear, informative, and include specific details
  to help users understand what is happening. Avoid vague messages that could cause
  confusion, and ensure proper stream handling to prevent garbled output in concurrent
  scenarios.
repository: nrwl/nx
label: Logging
language: TypeScript
comments_count: 2
repository_stars: 27518
---

Log messages should be clear, informative, and include specific details to help users understand what is happening. Avoid vague messages that could cause confusion, and ensure proper stream handling to prevent garbled output in concurrent scenarios.

When logging status or waiting messages, include the specific values or URLs being referenced:

```typescript
// Bad - vague and potentially confusing
console.log('Waiting for registry configuration to change from default...');

// Good - includes specific information
console.log('Waiting for registry configuration to change from https://registry.npmjs.org/...');
```

For concurrent processes that write to stdout/stderr, implement proper stream management to prevent output corruption:

```typescript
// Use LineAwareStream or similar mechanisms to ensure complete lines
task.childProcess.stdout?.on('data', (data) => {
  globalLineAwareStream.write(data, task.id);
});
```

This prevents garbled output when multiple processes are writing simultaneously and ensures logs remain readable and useful for debugging.