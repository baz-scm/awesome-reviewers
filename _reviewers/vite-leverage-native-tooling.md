---
title: Leverage native tooling
description: Prioritize native or Rust-based implementations of build tools over their
  JavaScript counterparts to significantly improve performance in both development
  and build phases. Tools like Rolldown (replacing Rollup and esbuild) can reduce
  build times and provide a more consistent experience between development and production
  environments.
repository: vitejs/vite
label: Performance Optimization
language: Markdown
comments_count: 4
repository_stars: 74031
---

Prioritize native or Rust-based implementations of build tools over their JavaScript counterparts to significantly improve performance in both development and build phases. Tools like Rolldown (replacing Rollup and esbuild) can reduce build times and provide a more consistent experience between development and production environments.

When developing plugins, utilize native performance features like hook filters to reduce overhead:

```js
// Example: Using hook filters in Rolldown plugins for better performance
const plugin = {
  name: 'my-performance-plugin',
  resolveId: {
    filter: /\.custom$/, // Only process specific files
    handler(source, importer) {
      // Handler only called for matching files, reducing JS-Rust communication overhead
      return this.resolve(source, importer);
    }
  }
}
```

For large applications, consider replacing multiple JavaScript-based tools with their native equivalents to create a more streamlined, performant pipeline. This approach reduces both build times and runtime overhead while maintaining compatibility with the existing ecosystem.