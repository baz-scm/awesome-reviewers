---
title: conditional component bundling
description: When adding conditional components to your application, ensure they are
  only bundled when actually needed to avoid unnecessary bundle bloat. This is especially
  important for optional features or components that depend on specific configurations.
repository: nuxt/nuxt
label: Next
language: Other
comments_count: 2
repository_stars: 57769
---

When adding conditional components to your application, ensure they are only bundled when actually needed to avoid unnecessary bundle bloat. This is especially important for optional features or components that depend on specific configurations.

Protect conditional components by checking if the feature is actually used before including the component. For example, if adding a component that only applies when certain route metadata exists, guard against always bundling it:

```vue
<!-- Bad: Always bundles NuxtPage even when not needed -->
<LazyNuxtPage v-else-if="route.meta?.isolate" />

<!-- Better: Only bundle when isolate metadata actually exists in routes -->
<LazyNuxtPage v-else-if="hasIsolateRoutes && route.meta?.isolate" />
```

This approach ensures that if no routes have the required metadata, there will be no changes to the bundle at all. Consider the trade-offs between lazy loading and bundle size, but prioritize avoiding unnecessary inclusions that impact all users regardless of feature usage.