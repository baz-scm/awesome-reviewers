---
title: Configure rendering modes clearly
description: Ensure clear distinction and proper handling between different rendering
  modes (SSR, SSG, SPA) with appropriate conditional logic for each mode's specific
  requirements.
repository: remix-run/react-router
label: Next
language: TypeScript
comments_count: 5
repository_stars: 55270
---

Ensure clear distinction and proper handling between different rendering modes (SSR, SSG, SPA) with appropriate conditional logic for each mode's specific requirements.

Different rendering modes have distinct behaviors and asset generation needs:
- **SPA Mode** (`ssr: false`, no prerender): Generates only a single `index.html` that can hydrate for any path
- **SSG Mode** (`ssr: false` + prerender paths): Generates multiple HTML pages, enabling loaders and build-time data
- **SSR Mode** (`ssr: true`): Handles rendering and manifests via server handler

Apply mode-specific logic consistently:

```typescript
function isSpaModeEnabled(reactRouterConfig) {
  // SPA Mode means we will only prerender a *single* `index.html` file
  // which prerenders only to the root route and can hydrate for _any_ path
  return (
    reactRouterConfig.ssr === false &&
    (reactRouterConfig.prerender == null || reactRouterConfig.prerender === false)
  );
}

// Conditionally remove exports based on rendering mode
if (!options?.ssr) {
  removeExports(ast, SERVER_ONLY_ROUTE_EXPORTS);
}

// Generate appropriate assets per mode
if (hasLoaders && isPrerenderingEnabled(reactRouterConfig)) {
  await prerenderData(handler, path, clientBuildDirectory);
}
```

This prevents configuration conflicts and ensures each mode generates the correct assets and applies the appropriate optimizations.