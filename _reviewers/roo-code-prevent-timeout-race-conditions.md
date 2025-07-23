---
title: Prevent timeout race conditions
description: When working with timeouts and asynchronous operations that affect shared
  state, clear timeouts at the beginning of event handlers or user interactions to
  prevent race conditions. This defensive approach ensures that competing operations
  (like auto-approval timers and manual user actions) don't conflict.
repository: RooCodeInc/Roo-Code
label: Concurrency
language: TSX
comments_count: 3
repository_stars: 17288
---

When working with timeouts and asynchronous operations that affect shared state, clear timeouts at the beginning of event handlers or user interactions to prevent race conditions. This defensive approach ensures that competing operations (like auto-approval timers and manual user actions) don't conflict.

Always implement shared cancellation mechanisms when multiple components or functions interact with the same asynchronous process:

```typescript
// GOOD: Clear timeouts at the beginning of handlers
function handleSendMessage(text, images) {
  // Clear auto-approval timeout FIRST to prevent race conditions
  if (autoApproveTimeoutRef.current) {
    clearTimeout(autoApproveTimeoutRef.current);
    autoApproveTimeoutRef.current = null;
  }
  
  // Now process the message safely
  if (messagesRef.current.length === 0) {
    vscode.postMessage({ type: "newTask", text, images });
  } else {
    // Other processing...
  }
}

// BAD: Clearing timeouts inside conditional blocks can lead to race conditions
function handleSendMessage(text, images) {
  if (messagesRef.current.length === 0) {
    vscode.postMessage({ type: "newTask", text, images });
  } else if (clineAskRef.current === "followup") {
    // Timeout might fire before reaching this point!
    if (autoApproveTimeoutRef.current) {
      clearTimeout(autoApproveTimeoutRef.current);
    }
    // Process message...
  }
}
```

For components with interdependent timers, consider using a shared state or context to coordinate cancellation across component boundaries.