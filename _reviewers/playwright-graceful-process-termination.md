---
title: graceful process termination
description: Implement systematic cleanup mechanisms that handle process termination
  signals without generating excessive error output. Use a generic disposable pattern
  to manage resources that need cleanup during exit, SIGINT, or other termination
  scenarios.
repository: microsoft/playwright
label: Error Handling
language: JavaScript
comments_count: 2
repository_stars: 76113
---

Implement systematic cleanup mechanisms that handle process termination signals without generating excessive error output. Use a generic disposable pattern to manage resources that need cleanup during exit, SIGINT, or other termination scenarios.

Create a centralized list of disposables (child processes, contexts, file handles) that can be properly disposed of during shutdown. This prevents error flooding in the terminal and ensures resources are cleaned up systematically.

Example implementation:
```javascript
const disposables = [];

// Register disposables
disposables.push(() => child.kill());
disposables.push(() => context.dispose());

// Handle termination signals
process.on('SIGINT', () => {
  disposables.forEach(dispose => dispose());
  cleanup();
});

process.on('exit', () => {
  disposables.forEach(dispose => dispose());
});
```

This approach prevents the terminal flooding with error messages like "exited with code null, signal SIGINT" while ensuring all resources are properly cleaned up during process termination.