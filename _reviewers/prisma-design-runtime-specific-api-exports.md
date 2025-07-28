---
title: Design runtime-specific API exports
description: When designing APIs that need to work across different JavaScript runtimes
  (Node.js, edge environments, browsers), create explicit export configurations that
  account for runtime-specific implementations. Different runtimes may require different
  API implementations that aren't interchangeable, so provide separate entry points
  rather than trying to create a...
repository: prisma/prisma
label: API
language: Json
comments_count: 2
repository_stars: 42967
---

When designing APIs that need to work across different JavaScript runtimes (Node.js, edge environments, browsers), create explicit export configurations that account for runtime-specific implementations. Different runtimes may require different API implementations that aren't interchangeable, so provide separate entry points rather than trying to create a one-size-fits-all solution.

Use package.json exports to define runtime-specific entry points:

```json
{
  "exports": {
    ".": {
      "require": {
        "types": "./dist/index-node.d.ts",
        "default": "./dist/index-node.js"
      },
      "import": {
        "types": "./dist/index-node.d.mts", 
        "default": "./dist/index-node.mjs"
      }
    },
    "./web": {
      "require": {
        "types": "./dist/index-web.d.ts",
        "default": "./dist/index-web.js"
      },
      "import": {
        "types": "./dist/index-web.d.mts",
        "default": "./dist/index-web.mjs"
      }
    }
  }
}
```

Make runtime-specific implementations opt-in rather than automatic to avoid confusion. Plan for ecosystem testing to verify that exports work correctly in target environments like Cloudflare Workers and Vercel Edge. When selecting dependencies, prefer libraries that provide ergonomic abstractions while maintaining broad runtime compatibility.