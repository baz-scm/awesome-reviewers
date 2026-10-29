---
title: Type definitions mirror runtime
description: Public type definitions (TypeScript, JSDoc, etc.) must precisely reflect
  the actual runtime contract of the API — no more permissive, no more restrictive,
  and no exposing capabilities that don't actually exist.
repository: chalk/chalk
label: API
language: TypeScript
comments_count: 4
repository_stars: 23342
---

Public type definitions (TypeScript, JSDoc, etc.) must precisely reflect the actual runtime contract of the API — no more permissive, no more restrictive, and no exposing capabilities that don't actually exist.

- Parameter and return types should match what the implementation actually accepts/produces. If a function coerces its arguments (e.g. via `String(x)`), type the parameter as `unknown`/`any` rather than `string`, since restricting it to `string[]` is misleading when any value works at runtime.
- Only expose properties/methods on an interface if they are genuinely available on that object at runtime. For example, if `supportsColor` only exists on the top-level default export and not on chained instances (`chalk.red.supportsColor`), it must not be declared as part of the shared `Chalk` interface — otherwise consumers get false type-checking guarantees. If such a property should logically exist everywhere, fix the runtime implementation first, then update the types to match.
- For fluent/chainable APIs, prefer `this` as the return type over the concrete class/interface name:
  ```ts
  rgb(r: number, g: number, b: number): this; // preferred
  // rgb(r: number, g: number, b: number): Chalk; // avoid
  ```
  This keeps subclassing and chaining type-safe and matches what the TS compiler itself generates.
- Extract shared shapes (e.g. `ColorSupport`, `ChalkConstructor`) into their own named interfaces instead of duplicating inline object types, improving readability and reuse.
- When keeping deprecated types/exports for backward compatibility, mark them clearly with `@deprecated` and a `TODO` noting removal in the next major version, so the deprecation has a concrete lifecycle instead of lingering indefinitely.

Treat the type definitions as a contract: any mismatch between declared types and actual behavior is a bug that should be fixed in either the runtime code or the types, never left inconsistent.