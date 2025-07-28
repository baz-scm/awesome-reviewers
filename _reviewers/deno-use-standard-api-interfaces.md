---
title: Use standard API interfaces
description: Always prefer established API interfaces and patterns over custom or
  alternative approaches. This ensures compatibility, maintainability, and follows
  expected conventions.
repository: denoland/deno
label: API
language: TypeScript
comments_count: 2
repository_stars: 103714
---

Always prefer established API interfaces and patterns over custom or alternative approaches. This ensures compatibility, maintainability, and follows expected conventions.

For module imports, use standard ESM syntax instead of dynamic loading:
```ts
// Preferred
import { assert } from "node:assert";

// Avoid
const assert = process.getBuiltinModule("node:assert");
```

For server interfaces, follow the established contract structure:
```ts
// Preferred
export default {
  fetch(req: Request) {
    return new Response("Hello from declarative server");
  },
  onListen(info) {
    console.log(info);
  }
} satisfies Deno.ServeDefaultExport;

// Avoid
export const fetch = (req: Request) => {
  return new Response("Hello from declarative server!");
};
```

This approach ensures your code works with existing tooling, follows documented patterns, and reduces the risk of breaking changes when alternative methods are deprecated.