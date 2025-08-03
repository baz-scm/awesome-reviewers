---
title: Prevent async deadlocks
description: Avoid circular dependencies in asynchronous code paths that can lead
  to deadlocks or indefinite blocking. When using async/await, ensure that promise
  chains have clear resolution paths and aren't dependent on their own completion.
  Be particularly careful with initialization patterns and refresh mechanisms.
repository: continuedev/continue
label: Concurrency
language: TypeScript
comments_count: 4
repository_stars: 27819
---

Avoid circular dependencies in asynchronous code paths that can lead to deadlocks or indefinite blocking. When using async/await, ensure that promise chains have clear resolution paths and aren't dependent on their own completion. Be particularly careful with initialization patterns and refresh mechanisms.

Example of problematic code:
```typescript
// PROBLEMATIC: Creates a deadlock
public async getSessions(): Promise<AuthSession[]> {
  await this.initialRefreshAttempt; // Waits for refresh to complete
  // ...
}

private async refreshSessions(): Promise<void> {
  const sessions = await this.getSessions(); // Calls getSessions which waits for refreshSessions
  // ...
}

constructor() {
  this.initialRefreshAttempt = this.refreshSessions();
}
```

Example of fixed code:
```typescript
// FIXED: Avoids deadlock by breaking circular dependency
public async getSessions(): Promise<AuthSession[]> {
  // Don't await initialRefreshAttempt here
  // ...
}

private async refreshSessions(): Promise<void> {
  const sessions = await this.getSessions();
  // ...
}

constructor() {
  this.initialRefreshAttempt = this.refreshSessions();
}
```

Additionally:
1. Always provide ways to cancel async operations (e.g., expose AbortController) to prevent resource leaks
2. Be careful with race conditions when checking state that might change during async operations
3. Analyze promise chains during code review to identify potential circular dependencies
4. Use centralized managers for coordinating related async operations when appropriate