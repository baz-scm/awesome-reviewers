---
title: Accurate null/undefined handling
description: "Make nullability explicit in types and handle it precisely instead of\
  \ papering over it with assumptions. \n\n1. Type signatures must reflect real-world\
  \ nullability. If a value can be `undefined` or `null` at runtime (e.g. `c.req.param('id')`,\
  \ a ref's initial value, a route path when no match exists), the type and tests\
  \ must say so instead of claiming a..."
repository: honojs/Hono
label: Null Handling
language: TypeScript
comments_count: 9
repository_stars: 32741
---

Make nullability explicit in types and handle it precisely instead of papering over it with assumptions. 

1. Type signatures must reflect real-world nullability. If a value can be `undefined` or `null` at runtime (e.g. `c.req.param('id')`, a ref's initial value, a route path when no match exists), the type and tests must say so instead of claiming a non-nullable type. Add overloads when behavior differs based on whether an argument/initial value is provided, e.g.:
```ts
export function useRef<T>(initialValue: T): RefObject<T>
export function useRef<T>(initialValue: T | null): RefObject<T | null>
export function useRef<T = undefined>(): RefObject<T | undefined>
```

2. Know the difference between "nullish" and "falsy" before reaching for `??` or `||`. `??` only catches `null`/`undefined`; it will not catch an intentionally-empty string, `0`, or `false`. When an empty value (like an empty string) has special meaning, check for it explicitly rather than relying on `??`:
```ts
// `??` won't treat '' as "missing" - check explicitly when empty string matters
const headerName = options?.headerName ?? 'X-Request-Id'
let requestId = headerName ? c.req.header(headerName) : undefined
```

3. Avoid redundant or unsafe null-handling. Don't double-guard a value that optional chaining already makes safe (e.g. spreading `undefined` is a no-op, so `...(args?.header ?? {})` can simply be `...args?.header`), and don't re-check a condition already guaranteed by an earlier check or type narrowing. Conversely, don't rely on non-null assertions (`!`) to silence the compiler when an explicit check is possible—prefer narrowing over assertion:
```ts
// Prefer this
const contentType = headers.get('Content-Type')
if (contentType !== null && contentType.startsWith('multipart/form-data')) { ... }

// over this
const contentType = headers.get('Content-Type')!
```

4. When a field's optionality in third-party/runtime data is inconsistent across versions or environments (e.g. AWS Lambda event headers, `multiValueHeaders`, API Gateway v1 vs v2 payloads), model it as optional in the type and guard each access independently; don't assume one field's presence implies another's, and don't use `else if` between independently-optional fields.

5. For "not found"/absent results, pick one consistent representation (e.g. returning `''` instead of `undefined` to preserve a non-nullable return type) and document it, rather than silently changing a function's return type or leaving the absent case undefined-but-untyped. Likewise, avoid introducing bugs where `undefined` is treated as "no cached value yet" versus a legitimately resolved `undefined` result—use a sentinel object/wrapper instead of relying on `undefined` as both "missing" and "empty" states.

Applying these rules prevents type-level lies, silent runtime bugs from falsy/nullish mixups, and either unsafe assertions or defensive-but-redundant null checks.