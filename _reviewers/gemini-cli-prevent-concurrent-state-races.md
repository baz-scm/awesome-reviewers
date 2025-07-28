---
title: Prevent concurrent state races
description: When multiple operations can execute concurrently (e.g., multiple keystrokes
  in the same React event loop, simultaneous async calls), ensure they don't operate
  on stale state or create race conditions. Use centralized state management patterns
  like reducers, proper synchronization flags, and avoid direct state manipulation
  from concurrent contexts.
repository: google-gemini/gemini-cli
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 65062
---

When multiple operations can execute concurrently (e.g., multiple keystrokes in the same React event loop, simultaneous async calls), ensure they don't operate on stale state or create race conditions. Use centralized state management patterns like reducers, proper synchronization flags, and avoid direct state manipulation from concurrent contexts.

**Key strategies:**
- **Use reducers for sequential operations**: When handling multiple rapid inputs, use a reducer pattern to ensure operations execute in proper order
- **Set synchronization flags synchronously**: Place flags like `this.flushing = true` immediately after condition checks, not inside async operations
- **Avoid reading state directly in concurrent contexts**: Don't read buffer state directly when multiple operations might modify it in the same event frame
- **Centralize state mutations**: Move state-changing logic into dedicated APIs rather than performing direct manipulations

**Example from vim input handling:**
```typescript
// ❌ Problematic: Direct state reading in concurrent context
const getCurrentOffset = useCallback(() => {
  const lines = buffer.lines; // Could be stale if multiple keystrokes processed
  // ... calculate offset
}, [buffer]);

// ✅ Better: Use reducer for sequential operations
const [state, dispatch] = useReducer(vimReducer, initialState);
// Operations go through reducer ensuring proper sequencing
```

**Example from async flag management:**
```typescript
// ❌ Race condition: Flag set inside async operation
async flushToClearcut() {
  this.flushing = true; // Too late - race window exists
  // ... async work
}

// ✅ Proper: Flag set synchronously after checks
flushIfNeeded() {
  if (this.flushing || /* other conditions */) return;
  this.flushing = true; // Set immediately after checks pass
  this.flushToClearcut().finally(() => this.flushing = false);
}
```

This prevents bugs where rapid user interactions or concurrent async operations interfere with each other, ensuring predictable behavior even under high-frequency input scenarios.