---
title: Vue component import handling
description: When working with Vue single-file components, pay special attention to
  how imports are processed, particularly with query parameters. URL handling can
  significantly impact module resolution and hot module replacement (HMR).
repository: vitejs/vite
label: Vue
language: TypeScript
comments_count: 2
repository_stars: 74031
---

When working with Vue single-file components, pay special attention to how imports are processed, particularly with query parameters. URL handling can significantly impact module resolution and hot module replacement (HMR).

Ensure proper handling of URLs with query parameters when importing Vue components to prevent duplicate entries in the module graph. For example, when a `.html?vue` file has additional query parameters like `&lang.js`, injecting further parameters (like `?import`) can cause issues.

```js
// Potentially problematic:
import Component from './Component.vue?custom=param&lang.js'

// Consider how query parameters are processed in your build tooling
// Be careful when manually adding parameters to imports
```

Also note that HMR behavior differs between file update, create, and delete operations. Custom HMR plugins only run on 'update' events by default, not on 'create' or 'delete'. When developing components that rely on HMR, test all file operations to ensure proper reactivity during development.