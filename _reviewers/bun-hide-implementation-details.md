---
title: Hide implementation details
description: When designing APIs, carefully consider which elements of your implementation
  become part of the public interface. Avoid exposing internal types, naming patterns,
  and implementation details that could confuse API consumers or lock you into supporting
  implementation details as part of your contract.
repository: oven-sh/bun
label: API
language: TypeScript
comments_count: 2
repository_stars: 79093
---

When designing APIs, carefully consider which elements of your implementation become part of the public interface. Avoid exposing internal types, naming patterns, and implementation details that could confuse API consumers or lock you into supporting implementation details as part of your contract.

For example, instead of exposing internal types in public modules:

```typescript
// Avoid this:
declare module "net" {
  type SocketHandleData = { self: Socket; req?: object };
  // Makes it look like a standard Node.js type
}

// Prefer this:
// Option 1: Move to your own namespace
declare module "bun" {
  namespace internal {
    type SocketHandleData = { self: Socket; req?: object };
  }
}

// Option 2: Inline the type where needed
interface Socket {
  _handle: { self: Socket; req?: object };
}
```

When dependencies might be deprecated or change, consider vendoring your own implementation rather than relying on shared code that might evolve independently:

```typescript
// Instead of depending on potentially changing shared implementations:
resultBindings.push(
  `    pub inline fn ${formatZigName(fn.name)}(...) {`,
  `        return bun.JSC.${callName}(...);`, // Depends on external implementation
  `    }`,
);
```