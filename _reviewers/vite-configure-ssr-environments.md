---
title: Configure SSR environments
description: When implementing server-side rendering in Next.js projects that use
  Vite as a bundler, ensure proper environment separation between client and server
  code. Create distinct module execution environments to prevent leaking server-only
  code to the client and to support hot module replacement (HMR) during development.
repository: vitejs/vite
label: Next
language: Markdown
comments_count: 2
repository_stars: 74031
---

When implementing server-side rendering in Next.js projects that use Vite as a bundler, ensure proper environment separation between client and server code. Create distinct module execution environments to prevent leaking server-only code to the client and to support hot module replacement (HMR) during development.

For custom SSR implementations with Next.js and Vite:

```js
// vite.config.js
export default {
  server: { 
    middlewareMode: true 
  },
  environments: {
    // Ensure proper Node.js environment for server components
    node: {
      dev: {
        createEnvironment: createNodeEnvironment,
      },
    },
  },
}

// server.js
const runner = createServerModuleRunner(server.environments.node)

// Use the runner for SSR with HMR support
const { render } = await runner.import('/src/entry-server.js')
```

This configuration helps maintain a clear separation between client and server environments, preventing server-side code from being exposed to the client while enabling HMR support for a smoother development experience with Next.js server components.