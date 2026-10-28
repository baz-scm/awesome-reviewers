---
title: Distinguish null from undefined
description: Null and undefined often carry distinct meanings (explicit clear vs.
  not provided vs. still loading), and code must preserve that distinction instead
  of treating them interchangeably with `??`, truthy checks, or loose equality. Validate
  and narrow untrusted/external values (API responses, wire payloads) to the exact
  expected type rather than trusting a type...
repository: cline/cline#|sleep 4
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70979
---

Null and undefined often carry distinct meanings (explicit clear vs. not provided vs. still loading), and code must preserve that distinction instead of treating them interchangeably with `??`, truthy checks, or loose equality. Validate and narrow untrusted/external values (API responses, wire payloads) to the exact expected type rather than trusting a type annotation: a server sending `null` where only `string | undefined` was expected can silently break loop-termination or retry logic. Watch for cases where a default parameter value swallows an explicit `undefined` argument — if you need "no override" to flow through such a parameter, pass `null` instead, and make sure the function signature actually says `| null`, not just `| undefined`. When a value is used as a sentinel for "clear this field" (e.g. `metadata: null`), make sure every layer (encode, transport, decode) preserves that sentinel instead of collapsing it to "omitted" or `{}`, which turns an intentional clear into a silent no-op. Finally, when an invariant you rely on (e.g. "artifacts is always set after this call") turns out to be null in some rare path, fail loudly (throw) rather than silently falling through into logic that assumes the invariant held.

Example of narrowing an external value instead of trusting its declared type:
```ts
// Before: null from the server satisfies `!== undefined` and spins forever
cursor = result.nextCursor;

// After: only a real string advances the loop; anything else (including null) stops it
cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined;
```