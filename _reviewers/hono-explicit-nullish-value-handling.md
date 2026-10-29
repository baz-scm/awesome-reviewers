---
title: Explicit nullish value handling
description: 'When dealing with optional, nullable, or possibly-missing values, handle
  them explicitly and avoid redundant or misleading fallback patterns:


  - Don''t add unnecessary fallbacks when the language already handles the case safely.
  For example, spreading `undefined` is a no-op, so `{ ...args?.header }` is sufficient;
  `{ ...(args?.header ?? {}) }` is redundant.'
repository: HONOJS/HONO
label: Null Handling
language: TypeScript
comments_count: 13
repository_stars: 32741
---

When dealing with optional, nullable, or possibly-missing values, handle them explicitly and avoid redundant or misleading fallback patterns:

- Don't add unnecessary fallbacks when the language already handles the case safely. For example, spreading `undefined` is a no-op, so `{ ...args?.header }` is sufficient; `{ ...(args?.header ?? {}) }` is redundant.
- Avoid double-defaulting the same value (e.g. giving a default in a function parameter and again when destructuring it), since this can silently override values the caller actually passed:
  ```ts
  // Bad: options.all/options.dot already resolved before destructuring, can override caller's input
  const { all = options?.all ?? false, dot = options?.dot ?? false } = options

  // Good: single point of truth for defaults
  export const parseBody = async (
    request: HonoRequest | Request,
    options: ParseBodyOptions = {}
  ) => {
    const { all = false, dot = false } = options
    ...
  }
  ```
- Choose the correct operator based on the actual semantics needed. `??` only triggers on `null`/`undefined`, `||` also triggers on falsy values like `''` or `false`. If an empty string or `false` is a meaningful, distinct value (e.g. "no header name" vs "use default header name"), handle it explicitly instead of relying on `??`:
  ```ts
  // headerName === '' means "disable the feature", which `??` won't catch
  let requestId = headerName ? c.req.header(headerName) : undefined
  ```
- When narrowing a union of types that may or may not have a given optional property, prefer explicit discriminants (e.g. an `in` check or a type-guard function) over chained optional access, which can silently resolve to `undefined` even when the property exists under a different shape:
  ```ts
  // Bad: silently undefined for APIGatewayProxyEventV2
  method: event.httpMethod ?? event.requestContext.http?.httpMethod

  // Good: explicit discrimination between event shapes
  const method = 'httpMethod' in event ? event.httpMethod : event.requestContext.http.method
  ```
- Avoid the non-null assertion operator (`!`) to silence the type checker; prefer explicit null checks or restructuring the logic so TypeScript can narrow the type on its own.
- When a value may legitimately be absent, decide on and document one consistent representation (e.g. always return `''` instead of mixing `undefined`/`null`/`''`) so the function's return type stays predictable (e.g. `string` instead of `string | undefined`) and callers don't need extra null checks.

Applying these practices prevents subtle bugs from incorrect fallback logic, keeps nullable/optional handling intentional, and reduces the need for non-null assertions and type casts.