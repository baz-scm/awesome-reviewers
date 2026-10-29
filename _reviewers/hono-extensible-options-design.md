---
title: Extensible options design
description: 'When adding configuration to middleware, helpers, or client functions,
  favor a single extensible options object over growing lists of positional parameters
  or narrow convenience flags. Concretely:'
repository: HONOJS/HONO
label: API
language: TypeScript
comments_count: 11
repository_stars: 32741
---

When adding configuration to middleware, helpers, or client functions, favor a single extensible options object over growing lists of positional parameters or narrow convenience flags. Concretely:

- Bundle related settings into one options object, and when adding new settings to an existing positional API, migrate to an options object while keeping backward compatibility via overloads, e.g.:
```ts
type VerifyOptions = { alg?: SignatureAlgorithm; issuer?: string | RegExp; audience?: string | string[] }
export const verify = async (
  token: string,
  publicKey: SignatureKey,
  algOrOptions?: SignatureAlgorithm | VerifyOptions
): Promise<JWTPayload> => {
  const options = typeof algOrOptions === 'string' ? { alg: algOrOptions } : algOrOptions ?? {}
  // ...
}
```
- Prefer a callback/predicate over a fixed list when the matching logic can't be fully enumerated, e.g. `contentTypesAsBinary: (contentType: string) => boolean` instead of `contentTypesAsBinary: string[]`. This lets users compose with sensible defaults instead of being locked into a static list.
- Pass the `Context` (or `Request`/`Response`) into user-supplied callbacks whenever useful, so consumers aren't limited to the data the option itself exposes (e.g. `onError?: (remote, c: Context) => Response`, `generator?: (c: Context) => string`, `generateParams?: (c: Context) => SSGParams`). For hooks that need both request and response, pass a single object (`{ request, response }`) rather than separate positional args, which also keeps the signature stable if more fields are added later.
- When two options are mutually exclusive, model them as one discriminated field instead of independent booleans, e.g. `prefix: 'host' | 'secure'` rather than `hostPrefix?: boolean; securePrefix?: boolean`.
- Accept both a single value and an array for list-like options to improve ergonomics, e.g. `vary?: string | string[]`.
- Before adding a dedicated convenience option, check whether it duplicates an existing general-purpose extension point (such as a success/error callback); if users can already achieve the same result with `onAuthSuccess: (c, username) => c.set('username', username)`, don't add a redundant `usernameContextKey` option.

Applying these guidelines keeps public APIs small, composable, and resilient to future growth, while still giving consumers the flexibility to handle edge cases themselves.