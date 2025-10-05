---
title: SSR documentation completeness
description: Ensure server-side rendering documentation provides complete implementation
  details with proper build configurations and explanatory context. SSR setup guides
  should include comprehensive Vite configurations that clearly separate client and
  server bundles, detailed explanations of script purposes, and complete file structures.
repository: TanStack/router
label: Next
language: Markdown
comments_count: 7
repository_stars: 11590
---

Ensure server-side rendering documentation provides complete implementation details with proper build configurations and explanatory context. SSR setup guides should include comprehensive Vite configurations that clearly separate client and server bundles, detailed explanations of script purposes, and complete file structures.

When documenting SSR setup:

1. **Include complete Vite configurations** with separate client/server build environments:
```ts
// vite.config.ts
const ssrBuildConfig: BuildEnvironmentOptions = {
  ssr: true,
  outDir: "dist/server",
  rollupOptions: {
    input: path.resolve(__dirname, "src/entry-server.tsx"),
    output: {
      entryFileNames: "[name].js",
      chunkFileNames: "assets/[name]-[hash].js",
    },
  },
};

const clientBuildConfig: BuildEnvironmentOptions = {
  outDir: "dist/client",
  rollupOptions: {
    input: path.resolve(__dirname, "src/entry-client.tsx"),
  },
};
```

2. **Provide explanatory context** for build processes and script purposes:
```json
{
  "scripts": {
    "build:client": "vite build",
    "build:server": "vite build --ssr"
  }
}
```
Add descriptions explaining that separate build processes ensure client and server bundles are served from distinct directories (dist/client and dist/server).

3. **Include complete file structures** showing root route configurations, entry points, and server setup with proper HTML document rendering patterns.

This ensures developers understand not just what to configure, but why each piece is necessary for proper SSR implementation.