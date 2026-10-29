---
title: Consistent, unambiguous naming
description: Choose identifier names that are unambiguous, self-explanatory, and consistent
  with existing conventions already used elsewhere in the codebase or in the relevant
  external spec/ecosystem. Before introducing a new name, check how similar concepts
  are named in sibling modules (e.g. other middlewares, adapters, generics) and reuse
  that convention rather than...
repository: honojs/Hono
label: Naming Conventions
language: TypeScript
comments_count: 15
repository_stars: 32741
---

Choose identifier names that are unambiguous, self-explanatory, and consistent with existing conventions already used elsewhere in the codebase or in the relevant external spec/ecosystem. Before introducing a new name, check how similar concepts are named in sibling modules (e.g. other middlewares, adapters, generics) and reuse that convention rather than inventing a new one.

Specifically:
- Prefer names whose meaning is unambiguous even without reading the docs. Avoid terms that can be read in opposite ways (e.g. `strict` was rejected because it was unclear whether `true` meant "always redirect" or "only on 404"; it was replaced with the explicit `alwaysRedirect`). Likewise avoid overloading well-known terms incorrectly (e.g. don't call something a "Factory" if it's a single function, not something that creates multiple instances — use `ExceptionFunction`/`HTTPExceptionFunction` instead).
- Reuse the same option/parameter name across similar APIs. If one middleware uses `headerName` to configure a header, a new middleware with the same concept should also use `headerName` rather than `header` or `authorization`.
- When exporting a named function for a middleware/handler, make sure the function's internal name matches its exported/public name (e.g. `export const languageDetector = ... return async function languageDetector(...)`), and always use a named function (not an anonymous one) so it's identifiable in stack traces/debugging tools.
- When introducing a type/option that is specific to this project (not part of a native/standard type), prefix it clearly (e.g. `HonoJsonWebKey` extends the standard `JsonWebKey`) and export it consistently from the shared types module.
- When wrapping or re-declaring web/platform APIs (HTML attributes, DOM options, etc.), match the exact casing/spelling defined by the official spec or MDN documentation rather than guessing (e.g. `srcdoc`, `datetime`, `disablePictureInPicture`).
- Use the same generic type parameter conventions already established in the codebase (e.g. `E` for `Env`, not `TEnv`) and keep naming consistent across platform-specific builds (e.g. keep `toSSG` consistent between `deno`/`bun` adapters instead of renaming per-platform).
- Double check for typos in exported names (e.g. `Uint` → `Unit`) since these become part of the public API and are hard to fix later.

Example:
```ts
// Bad: ambiguous option name, anonymous function, inconsistent with sibling middleware
export const myMiddleware = (options: { authorization?: string; strict?: boolean }) => {
  return async (c, next) => { ... }
}

// Good: name matches existing convention, named function, avoids ambiguity
export const myMiddleware = (options: { headerName?: string; alwaysRedirect?: boolean }) => {
  return async function myMiddleware(c, next) { ... }
}
```

Applying this standard reduces confusion during code review, prevents churn from repeated renames, and keeps the public API coherent across the whole library.