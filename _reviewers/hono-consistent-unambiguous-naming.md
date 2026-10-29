---
title: Consistent, unambiguous naming
description: Names must be consistent with existing conventions elsewhere in the codebase
  and must clearly convey their purpose and scope, avoiding ambiguity or collisions.
repository: honojs/hono
label: Naming Conventions
language: TypeScript
comments_count: 17
repository_stars: 32741
---

Names must be consistent with existing conventions elsewhere in the codebase and must clearly convey their purpose and scope, avoiding ambiguity or collisions.

Apply the following when naming identifiers:
- Reuse the naming pattern already established for similar concepts instead of inventing a new one. For example, use `headerName` to match the JWT middleware instead of introducing `authorization`, use the generic parameter `E` instead of `TEnv` to match the rest of the codebase, and keep platform-specific exports like `toSSG` consistent across adapters rather than renaming per-platform (`toDenoSSG`).
- Prefer explicit, descriptive names over shortening or reusing a borrowed/external name verbatim. Internal utility names can stay short if well-documented, but publicly exported or widely-used identifiers should describe what they do (e.g., prefer `headerName`-style clarity over a playful name like `fetchRP` without context).
- Avoid names that are ambiguous about their scope or usage. If an option/property applies to only part of a larger API surface, name it accordingly (e.g., `defaultAppOptions` instead of `defaultOptions` on a `Factory` that also creates middleware and handlers).
- Do not let a parameter shadow the name of its enclosing function or another identifier in scope; pick a distinct name (e.g., rename a `generateDigest` parameter to `generator` inside a `generateDigest` function).
- When extending or wrapping a well-known external type, prefix it with the project name to signal the difference (e.g., `HonoJsonWebKey` extending `JsonWebKey`), and export such types from a shared location if they're used across multiple modules.
- For generic/compound type fields whose names could be confused with each other (e.g., an `Input` type with both `input` and `output` keys), pick short, distinct names that reduce ambiguity, such as `in`/`out`.
- All middleware and handlers returned from factory functions must be named function expressions, not anonymous functions, so the name is visible for debugging/dev tooling:
```ts
// Good
export const contextStorage = (): MiddlewareHandler => {
  return async function contextStorage(c, next) {
    ...
  }
}

// Avoid
export const contextStorage = (): MiddlewareHandler => {
  return async (c, next) => {
    ...
  }
}
```
- When modeling well-known external specs (e.g., native HTML attributes), match the external casing/spelling convention exactly (e.g., `srcdoc`, `datetime` as lowercase HTML attributes) while keeping JS-only/non-standard properties in camelCase (e.g., `disablePictureInPicture`, `disableRemotePlayback`).

Following these rules keeps the API surface predictable, reduces confusion for both maintainers and consumers, and makes debugging easier.