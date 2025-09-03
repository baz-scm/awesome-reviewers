---
title: consolidate build scripts
description: When creating multiple build variants (debug, publish, etc.), avoid duplicating
  build commands by reusing the base build script. This reduces maintenance overhead,
  ensures consistency across build targets, and shortens complex build commands.
repository: menloresearch/jan
label: CI/CD
language: Json
comments_count: 2
repository_stars: 37620
---

When creating multiple build variants (debug, publish, etc.), avoid duplicating build commands by reusing the base build script. This reduces maintenance overhead, ensures consistency across build targets, and shortens complex build commands.

Instead of duplicating the entire build process in each script:
```json
{
  "build": "tsc -b . && webpack --config webpack.config.js",
  "build:publish": "tsc -b . && webpack --config webpack.config.js && rimraf *.tgz --glob && npm pack && cpx *.tgz ../../electron/core/pre-install"
}
```

Consolidate by referencing the base build command:
```json
{
  "build": "tsc -b . && webpack --config webpack.config.js",
  "build:publish": "npm run build && rimraf *.tgz --glob && npm pack && cpx *.tgz ../../electron/core/pre-install"
}
```

This approach ensures that changes to the base build process automatically propagate to all build variants, reducing the risk of inconsistencies and making the build pipeline more maintainable.