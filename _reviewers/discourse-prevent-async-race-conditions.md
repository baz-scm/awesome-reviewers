---
title: Prevent async race conditions
description: When handling multiple concurrent async operations (like user input triggering
  API calls or messageBus updates), implement mechanisms to prevent race conditions
  where stale results could overwrite newer state.
repository: discourse/discourse
label: Concurrency
language: Other
comments_count: 2
repository_stars: 44898
---

When handling multiple concurrent async operations (like user input triggering API calls or messageBus updates), implement mechanisms to prevent race conditions where stale results could overwrite newer state.

Use request IDs to track and validate async operations:

```javascript
async fetchSuggestions() {
  const input = this.currentInputValue || "";
  const requestId = ++this.suggestionRequestId;
  
  const results = await this.suggester.search(input);
  
  // Only process if this is still the latest request
  if (requestId === this.suggestionRequestId) {
    this.suggestions = results;
  }
}
```

Alternatively, use AbortController to cancel outdated requests:

```javascript
async fetchSuggestions() {
  // Cancel previous request
  if (this.abortController) {
    this.abortController.abort();
  }
  
  this.abortController = new AbortController();
  const results = await this.suggester.search(input, { 
    signal: this.abortController.signal 
  });
  
  this.suggestions = results;
}
```

This prevents scenarios where fast user interactions or component state changes could result in displaying incorrect data from slower, outdated async operations.