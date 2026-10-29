---
title: Design extensible, composable option APIs
description: 'When designing public APIs for middleware, helpers, and client functions,
  favor extensible, composable configuration over ad-hoc parameters that are hard
  to grow later:'
repository: honojs/Hono
label: API
language: TypeScript
comments_count: 12
repository_stars: 32741
---

When designing public APIs for middleware, helpers, and client functions, favor extensible, composable configuration over ad-hoc parameters that are hard to grow later:

- Prefer a single options object over multiple positional arguments once more than one or two parameters are involved, and support function overloads to keep backward compatibility when migrating an existing positional API. For example, instead of `verify(token, key, alg, issuer)`, grow toward `verify(token, key, { alg, issuer, audience })` with an overload that still accepts the old `alg` string.
- When a behavior may need to vary per call (matching content types, generating IDs, building error responses, deciding what to retain/forward), accept a callback instead of a fixed primitive (string, array, boolean), e.g. `contentTypesAsBinary: (contentType) => boolean` or `timeout(duration, (c) => new HTTPException(...))`. Callbacks give consumers full flexibility without the library needing to anticipate every case.
- Pass the `Context` (or `Request`/`Response`, as appropriate) into these callbacks so consumers can access route params, env bindings, and app state instead of being limited to primitive inputs, e.g. `onError: (remote, c) => ...`, `generator: (c) => string`, `generateParams: (c) => SSGParams`.
- Before adding a narrow, single-purpose option, check whether it can already be achieved by composing existing extension points (hooks/callbacks/context setters). If `onAuthSuccess: (c, username) => c.set('user', username)` already covers a use case, don't also add a dedicated `usernameContextKey` option — extra options multiply the surface area and maintenance cost without adding real capability.
- Accept both a single value and an array where it is natural for ergonomics (`vary?: string | string[]`) rather than forcing consumers to always wrap a single value.

Applying these principles keeps Hono's own APIs small, predictable, and future-proof: new capabilities can be layered in via callbacks and options objects without breaking changes, and redundant one-off knobs are avoided in favor of a few well-designed extension points.