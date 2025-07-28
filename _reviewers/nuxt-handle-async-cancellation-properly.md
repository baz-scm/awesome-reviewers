---
title: Handle async cancellation properly
description: When implementing async operations with cancellation support, ensure
  that cancelled operations do not continue to update application state and that all
  cleanup logic is properly consolidated. This prevents race conditions where cancelled
  requests might still modify data after cancellation.
repository: nuxt/nuxt
label: Concurrency
language: TypeScript
comments_count: 4
repository_stars: 57769
---

When implementing async operations with cancellation support, ensure that cancelled operations do not continue to update application state and that all cleanup logic is properly consolidated. This prevents race conditions where cancelled requests might still modify data after cancellation.

Key practices:
1. **Track cancellation state**: Set a cancelled flag when abort controllers are triggered, both from internal clear() calls and external abort signals
2. **Prevent state updates**: Check cancellation status before updating data/status to avoid processing results from cancelled operations  
3. **Consolidate cleanup**: Group related cleanup logic in existing disposal handlers rather than creating multiple separate listeners
4. **Handle async cleanup limitations**: Be aware that async cleanup hooks may not work reliably in all environments (e.g., Windows process termination)

Example implementation:
```ts
clear: () => {
  if (options.abortController) {
    options.abortController.abort(new DOMException('Request aborted as the async data was cleared.', 'AbortError'))
  }
  if (nuxtApp._asyncDataPromises[key.value]) {
    (nuxtApp._asyncDataPromises[key.value] as any).cancelled = true
  }
}

// Listen for external cancellation
options.abortController.signal.addEventListener('abort', () => {
  if (nuxtApp._asyncDataPromises[key.value]) {
    (nuxtApp._asyncDataPromises[key.value] as any).cancelled = true
  }
})

// Consolidate cleanup in existing disposal handler
if (hasScope) {
  onScopeDispose(() => {
    off()
    stopPolling() // Add to existing handler rather than creating new one
  })
}
```