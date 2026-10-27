---
title: Design extensible options objects
description: When a public or semi-public API takes multiple parameters (especially
  booleans or flags), use a named options object rather than positional arguments.
  This keeps call sites readable, avoids ambiguity when toggling multiple flags, and
  makes it easy to add new options later without breaking existing call sites (e.g.
  public tool schemas should take an object...
repository: facebook/react#b18
label: API
language: JavaScript
comments_count: 4
repository_stars: 251889
---

When a public or semi-public API takes multiple parameters (especially booleans or flags), use a named options object rather than positional arguments. This keeps call sites readable, avoids ambiguity when toggling multiple flags, and makes it easy to add new options later without breaking existing call sites (e.g. public tool schemas should take an object of named arguments rather than relying on positional booleans).

When forwarding an options object from a public API into an internal dispatcher or implementation, type the internal signature to require all known fields (e.g. `options?: Required<PreloadModuleImplOptions>`) instead of leaving them all optional. This forces every call site to explicitly pass each field, preventing silent omissions when new options are added to the public API but forgotten in the forwarding call.

Conversely, when defining a type that will be part of a public contract (e.g. a response/headers descriptor), mark fields optional if there's any chance they won't always be populated in future versions — don't lock callers into assuming a field will always be present.

Finally, make sure the semantics of each option match the real contract it models (e.g. DOM spec treats `passive`/`once` as non-identity attributes for event listeners, so they must not be encoded into any identity/key logic). Verify option behavior against the authoritative spec or contract, not just intuition, before encoding it into the API's internal representation.