---
title: API overload design
description: 'When an API exposes multiple optional parameters or several overloaded
  signatures, design them deliberately for type-safety and clarity rather than convenience
  typing. Concretely:'
repository: tj/commander.js#CANARY-1ebfbbf4
label: API
language: TypeScript
comments_count: 5
repository_stars: 28444
---

When an API exposes multiple optional parameters or several overloaded signatures, design them deliberately for type-safety and clarity rather than convenience typing. Concretely:

1. Avoid `any` in public signatures when a more specific type (e.g. `string | boolean`, or a generic `T`) can preserve compile-time checking. Loose `any` parameters silently defeat the purpose of TypeScript typings.
2. When providing multiple overloads, order them from most specific to least specific (and/or most common case first), since TypeScript resolves the first matching overload. A trailing overload using `any`/all-optional parameters can accidentally swallow calls meant for a more specific overload, so it must come last:
```ts
// correct: boolean/string case first, regexp-fn overloads next, loose fallback last
option(flags: string, description?: string, defaultValue?: string | boolean): Command;
option<T>(flags: string, description: string, fn: (value: string, previous: T) => T, defaultValue?: T): Command;
option(flags: string, description: string, regexp: RegExp, defaultValue?: string): Command;
```
3. When a function accumulates many optional parameters (especially booleans/numbers with related meaning), replace the positional parameter list with an options object. This self-documents the call site and lets callers specify only the options they need:
```ts
// instead of: wrap(str, width, indent, minColumnWidth, overflowShift, globalIndent, columnGap)
wrap(str, width, { minWidthGuideline: 20 });
```
4. Keep type signatures (including callback parameter types) accurate and in sync with actual runtime behavior; do not leave stale or overly generic types (e.g. `(str: string) => string` when the implementation only returns `void`).

Applying these rules keeps the public API type-safe, predictable under overload resolution, and easy to call correctly.