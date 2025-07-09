---
title: React transformation tool clarity
description: When working with React in Vite projects, be precise about which transformation
  tools (Babel, SWC, Oxc, esbuild) handle specific aspects of React code processing.
  Different plugins use different tool combinations for JSX/TSX transformation versus
  React fast-refresh, and these can vary between development and build environments.
repository: vitejs/vite
label: React
language: Markdown
comments_count: 2
repository_stars: 74031
---

When working with React in Vite projects, be precise about which transformation tools (Babel, SWC, Oxc, esbuild) handle specific aspects of React code processing. Different plugins use different tool combinations for JSX/TSX transformation versus React fast-refresh, and these can vary between development and build environments.

For example, when documenting or selecting a React plugin:

```js
// Document precisely which tools handle which transformations
// @vitejs/plugin-react (without plugins)
//   - dev: Babel (fast-refresh) + esbuild/Oxc (JSX)
//   - build: esbuild/Oxc (JSX)

// @vitejs/plugin-react-swc (without plugins)
//   - dev: SWC (fast-refresh + JSX)
//   - build: esbuild/Oxc (JSX)

// @vitejs/plugin-react-oxc
//   - dev: Oxc (fast-refresh + JSX)
//   - build: Oxc (JSX)
```

This distinction is particularly important when migrating between plugins or when performance optimization is needed. Always verify compatibility with your project's requirements, especially when using custom Babel or SWC configurations.