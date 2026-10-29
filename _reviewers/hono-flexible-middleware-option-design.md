---
title: Flexible middleware option design
description: 'When designing options and callbacks for middleware/helpers, favor extensible,
  composable patterns over narrow, single-purpose additions.


  - Pass the `Context` (or relevant request data) into user-supplied callbacks whenever
  behavior may depend on the request, so users can implement custom logic without
  new options (e.g. `onError: (remote, c: Context) =>...'
repository: honojs/hono
label: API
language: TypeScript
comments_count: 11
repository_stars: 32741
---

When designing options and callbacks for middleware/helpers, favor extensible, composable patterns over narrow, single-purpose additions.

- Pass the `Context` (or relevant request data) into user-supplied callbacks whenever behavior may depend on the request, so users can implement custom logic without new options (e.g. `onError: (remote, c: Context) => ...`, `generator: (c: Context) => string`, `ssgParams(async (c) => ...)`).
- Accept both a plain value and a function/array where it increases flexibility, e.g. `vary?: string | string[]`, or `contentTypesAsBinary?: (contentType: string) => boolean` instead of only `string[]`.
- Use a discriminated union instead of multiple independent booleans when only one option can be meaningfully active at a time, e.g. prefer `prefix?: 'host' | 'secure'` over `securePrefix?: boolean; hostPrefix?: boolean`.
- Don't add a narrow convenience option if an existing generic hook/callback already covers the use case cleanly (e.g. reject `usernameContextKey` because `onAuthSuccess: (c, username) => c.set(...)` already solves it) — keep the public option surface minimal.
- When a helper ships default configuration (e.g. a MIME-to-extension map), export the default so users can spread/extend it (`{ ...defaultExtensionMap, 'application/foo': 'foo' }`) instead of only allowing full replacement.
- Prefer combining many related, growing parameters into a single options object with sane defaults and, if needed, an overload for backward compatibility, rather than continuously appending positional arguments (e.g. JWT `verify(token, key, options: VerifyOptions)` instead of `verify(token, key, alg, issuer, audience, ...)`).

Applying these principles keeps public APIs predictable, avoids combinatorial option explosion, and gives consumers enough flexibility to handle edge cases without requiring new library changes.