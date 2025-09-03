---
title: ensure async synchronization
description: When dealing with async operations that depend on external systems (servers,
  backends, etc.), ensure proper synchronization to avoid race conditions. Don't rely
  on client-side polling or workarounds when the root cause is improper async handling.
repository: cypress-io/cypress
label: Concurrency
language: Other
comments_count: 2
repository_stars: 48850
---

When dealing with async operations that depend on external systems (servers, backends, etc.), ensure proper synchronization to avoid race conditions. Don't rely on client-side polling or workarounds when the root cause is improper async handling.

Key principles:
- Make functions async when they need to wait for external operations to complete
- Use proper sequencing for initialization dependencies
- Ensure server acknowledgment before proceeding with dependent operations

Example of proper async sequencing:
```js
// Instead of client-side polling workarounds
async function start(openElectron) {
  await initializeThings()
  openElectron()
}

// Make functions async when they need to ensure completion
async function reset() {
  await Cypress.backend("set:traffic:routing:reset")
}
```

This prevents race conditions where the UI renders before the backend is ready, or where operations proceed without confirming the previous step completed successfully.