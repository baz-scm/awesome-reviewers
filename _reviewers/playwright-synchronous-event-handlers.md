---
title: Synchronous event handlers
description: Keep event handlers synchronous to prevent race conditions and timing
  issues. Async operations within event handlers can cause deadlocks, missed events,
  and unpredictable behavior.
repository: microsoft/playwright
label: Concurrency
language: TypeScript
comments_count: 5
repository_stars: 76113
---

Keep event handlers synchronous to prevent race conditions and timing issues. Async operations within event handlers can cause deadlocks, missed events, and unpredictable behavior.

**Why this matters:**
Event handlers must execute synchronously to ensure proper event ordering and prevent race conditions. When async operations are introduced into event handlers, they can cause events to be missed, create deadlocks with message passing, or lead to cleanup operations happening at the wrong time.

**Guidelines:**
1. **Never make event handlers async** - Event callbacks should complete synchronously
2. **Defer async work** - If async operations are needed, schedule them separately rather than awaiting in the handler
3. **Be careful with cleanup timing** - Removing event listeners immediately can prevent clients from receiving events

**Example of problematic pattern:**
```javascript
// BAD: Async event handler can cause timing issues
private async _onPage(page: Page): Promise<void> {
    this._pages.add(page);
    this.emit(Events.BrowserContext.Page, page);
    await this._mockingProxy?.instrumentPage(page); // This breaks synchronous event flow
}

// BAD: Immediate cleanup prevents event delivery
close() {
    this._socket.close();
    eventsHelper.removeEventListeners(this._eventListeners); // Client never receives 'close' event
}
```

**Better approach:**
```javascript
// GOOD: Keep handler synchronous, defer async work
private _onPage(page: Page): void {
    this._pages.add(page);
    this.emit(Events.BrowserContext.Page, page);
    // Schedule async work separately
    this._instrumentPageAsync(page);
}

private async _instrumentPageAsync(page: Page) {
    await this._mockingProxy?.instrumentPage(page);
}
```

This principle prevents deadlocks, ensures event ordering, and maintains predictable async behavior throughout the application.