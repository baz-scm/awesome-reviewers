---
title: Ensure documentation accuracy
description: 'Documentation must precisely reflect the current codebase implementation.
  When documenting features, options, or APIs:


  1. Validate that all examples match the actual implementation. For instance, if
  template names or file formats change, update all references in the documentation:'
repository: vitejs/vite
label: Documentation
language: Markdown
comments_count: 6
repository_stars: 74031
---

Documentation must precisely reflect the current codebase implementation. When documenting features, options, or APIs:

1. Validate that all examples match the actual implementation. For instance, if template names or file formats change, update all references in the documentation:

```diff
- Package manager lockfile content, e.g. `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` or `bun.lockb`.
+ Package manager lockfile content, e.g. `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lock`, or `bun.lockb`.
```

2. Remove outdated conditional language when options change. Instead of "can also be", use definitive statements that reflect current functionality:

```diff
- The value can also be an [options object] passed to `https.createServer()`.
+ The value is an [options object] passed to `https.createServer()`.
```

3. Remove deprecated parameters from examples and clarify their status in API references:

```diff
 interface ModuleRunnerOptions {
   /**
    * Root of the project
+   * @deprecated not used anymore and to be removed
    */
-  root: string
+  root?: string
 }
```

4. When updating or renaming APIs, ensure all documentation consistently uses the new terminology throughout. Maintaining accuracy builds user trust and prevents confusion when implementing features.