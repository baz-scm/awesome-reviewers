---
title: dependency management practices
description: 'Ensure comprehensive dependency management in package.json files by
  following these practices:


  1. **Evaluate necessity**: Before adding dependencies, check if native Node.js APIs
  provide the functionality. For example, use `fs.mkdtemp(path.join(os.tmpdir(), ''prefix''))`
  instead of adding a temporary file library.'
repository: rocicorp/mono
label: Configurations
language: Json
comments_count: 4
repository_stars: 2091
---

Ensure comprehensive dependency management in package.json files by following these practices:

1. **Evaluate necessity**: Before adding dependencies, check if native Node.js APIs provide the functionality. For example, use `fs.mkdtemp(path.join(os.tmpdir(), 'prefix'))` instead of adding a temporary file library.

2. **Choose appropriate dependency types**: Carefully classify dependencies as `dependencies`, `devDependencies`, or `peerDependencies` based on their usage. When uncertain about peer dependencies in monorepos, start with `devDependencies` and adjust as needed.

3. **Use consistent versioning**: Establish a clear strategy for version specifications - either pin exact versions (`"esbuild": "0.25.0"`) or use ranges (`"esbuild": "^0.25.0"`) consistently across the project.

4. **Update all related files**: When modifying package.json, ensure package-lock.json is also updated and included in commits.

Example of proper dependency evaluation:
```js
// Instead of adding a dependency like 'tmp'
"dependencies": {
  "tmp": "^0.2.3"
}

// Use native Node.js APIs
fs.mkdtemp(path.join(os.tmpdir(), 'myapp-'));
```

This approach reduces dependency bloat, minimizes security vulnerabilities, and maintains cleaner, more maintainable projects.