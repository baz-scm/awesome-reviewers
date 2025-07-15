---
title: Document code purposefully
description: 'High-quality code documentation improves maintainability and helps other
  developers understand your intentions. Follow these practices:


  1. **Use appropriate JSDoc annotations** to indicate API visibility and status:'
repository: vitejs/vite
label: Documentation
language: TypeScript
comments_count: 4
repository_stars: 74031
---

High-quality code documentation improves maintainability and helps other developers understand your intentions. Follow these practices:

1. **Use appropriate JSDoc annotations** to indicate API visibility and status:
   ```typescript
   /** @internal */
   hostname: Hostname
   
   /**
    * @deprecated Use `createIdResolver` from `vite` instead.
    */
   ```

2. **Structure API documentation logically** by describing functionality first, then providing implementation details or deprecation notices:
   ```typescript
   /**
    * Create an internal resolver to be used in special scenarios, e.g.
    * optimizer & handling css `@imports`.
    *
    * This API is deprecated. It only works for the client and ssr
    * environments. The `aliasOnly` option is also not being used anymore.
    * Plugins should move to `createIdResolver(environment.config)` instead.
    */
   ```

3. **Add explanatory comments for non-obvious code decisions** to explain the "why" behind implementation choices:
   ```typescript
   // only limit to these extensions because:
   // - for the `@import`/`@use`s written in file loaded by `load` function,
   //   the `canonicalize` function of that `importer` is called first
   // - the `load` function of an importer is only called for the importer
   //   that returned a non-null result from its `canonicalize` function
   (resolved.endsWith('.css') || resolved.endsWith('.scss') || resolved.endsWith('.sass'))
   ```

4. **Keep documentation updated** when implementing changes, especially for deprecated features. Explicitly indicate migration paths and alternatives when deprecating functionality.