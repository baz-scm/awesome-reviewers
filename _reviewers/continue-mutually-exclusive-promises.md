---
title: Mutually exclusive promises
description: Ensure that promises are either resolved or rejected, but never both.
  When handling promise resolution in callbacks or event handlers, use proper conditional
  logic to guarantee mutual exclusion between success and error paths.
repository: continuedev/continue
label: Error Handling
language: JavaScript
comments_count: 2
repository_stars: 27819
---

Ensure that promises are either resolved or rejected, but never both. When handling promise resolution in callbacks or event handlers, use proper conditional logic to guarantee mutual exclusion between success and error paths.

For example, this pattern creates inconsistent promise states:
```javascript
return new Promise((resolve, reject) => {
  child.on("message", (msg) => {
    if (msg.error) {
      reject();
    }
    resolve(); // Problem: This always executes regardless of error state
  });
});
```

Instead, use an else block to ensure mutual exclusion:
```javascript
return new Promise((resolve, reject) => {
  child.on("message", (msg) => {
    if (msg.error) {
      reject();
    } else {
      resolve(); // Correct: Only resolves if there is no error
    }
  });
});
```

This prevents inconsistent promise states where both error and success handlers might execute, leading to unpredictable application behavior and hard-to-debug issues.