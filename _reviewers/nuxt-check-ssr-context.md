---
title: Check SSR context
description: Always verify execution context (server vs client) before running client-specific
  operations in SSR applications. Many hydration errors and unexpected behaviors stem
  from client-only code executing during server-side rendering.
repository: nuxt/nuxt
label: Next
language: TypeScript
comments_count: 3
repository_stars: 57769
---

Always verify execution context (server vs client) before running client-specific operations in SSR applications. Many hydration errors and unexpected behaviors stem from client-only code executing during server-side rendering.

Key practices:
- Use `import.meta.client` checks before client-specific operations like polling, timers, or browser APIs
- Ensure context availability before using composables that depend on client state
- Be aware that some operations like `useHead()` may not work properly in server components without proper context

Example from polling implementation:
```ts
const startPolling = () => {
  if (import.meta.client && options.pollEvery && !pollTimer) {
    // Client-only polling logic
  }
}
```

This prevents server-side execution of client-specific code and reduces hydration mismatches that can break SSR applications.