---
title: Configuration option consistency
description: Ensure configuration options follow consistent naming conventions and
  are documented accurately. Use "default" prefix for options that can be overridden
  at more specific levels (e.g., `defaultOutputPath` instead of `outputPath`). Document
  only public APIs - avoid documenting internal or experimental configuration options
  that are not yet part of the public...
repository: TanStack/router
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 11590
---

Ensure configuration options follow consistent naming conventions and are documented accurately. Use "default" prefix for options that can be overridden at more specific levels (e.g., `defaultOutputPath` instead of `outputPath`). Document only public APIs - avoid documenting internal or experimental configuration options that are not yet part of the public interface. Provide clear, grammatically correct descriptions for all configuration options, including proper property names and examples.

Example of consistent naming:
```ts
// Good - follows default + override pattern
export default defineConfig({
  codeSplittingOptions: {
    defaultBehavior: [['component'], ['errorComponent']], // Global default
    splitBehavior: ({ routeId }) => { /* per-route override */ }
  }
})

// Bad - unclear relationship between global and specific options  
export default defineConfig({
  codeSplittingOptions: {
    outputPath: (path) => path, // Should be defaultOutputPath
  }
})
```

This ensures developers can easily understand configuration hierarchies and reduces confusion about which options are available and how they interact.