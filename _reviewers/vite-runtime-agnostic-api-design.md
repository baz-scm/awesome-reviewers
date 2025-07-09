---
title: Runtime-agnostic API design
description: When designing APIs for systems that support multiple JavaScript runtimes,
  prioritize decoupling server state from user modules. This approach enables code
  to run consistently across different environments (Node.js, browsers, edge runtimes)
  without relying on runtime-specific features.
repository: vitejs/vite
label: API
language: Markdown
comments_count: 5
repository_stars: 74031
---

When designing APIs for systems that support multiple JavaScript runtimes, prioritize decoupling server state from user modules. This approach enables code to run consistently across different environments (Node.js, browsers, edge runtimes) without relying on runtime-specific features.

Instead of directly accessing server state from user modules:

```ts
// Anti-pattern: Tightly coupling server and user code
const vite = createServer()
const { processRoutes } = await vite.ssrLoadModule('internal:routes-processor')
processRoutes(collectRoutes()) // Server state leaks into user module
```

Use virtual modules to mediate between server and user code:

```ts
// Recommended: Decoupled through virtual modules
function vitePlugin() {
  return {
    name: 'virtual-data-provider',
    resolveId(source) {
      return source === 'virtual:app-data' ? '\0' + source : undefined
    },
    async load(id) {
      if (id === '\0virtual:app-data') {
        return `export const data = ${JSON.stringify(serverData)}`
      }
    }
  }
}

// In user module:
import { data } from 'virtual:app-data'
// Process data without direct server dependency
```

For communication between environments, prefer structured APIs with clear transport abstractions rather than relying on shared runtime contexts. If runtime-specific features are needed, isolate them in well-defined interfaces that can be implemented differently across environments.

This pattern enables your code to run in any JavaScript runtime with minimal adaptation, making it suitable for environments like Cloudflare Workers, Deno, browsers, or Node.js servers.