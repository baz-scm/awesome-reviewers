---
title: Design Stable API Contracts
description: 'When an API is public (devtools tools, client/server entrypoints, SSR
  helpers) or schema-driven, design its contract to be stable, explicit, and compatible:'
repository: facebook/react#b17
label: API
language: JavaScript
comments_count: 8
repository_stars: 251891
---

When an API is public (devtools tools, client/server entrypoints, SSR helpers) or schema-driven, design its contract to be stable, explicit, and compatible:

- Prefer **options bags** over expanding positional args. Keep optional fields as named properties so callers can evolve without ambiguity.
- Avoid **mode explosion** in a single function signature (many arguments that subtly change behavior). Use **variant-specific functions** or **separate entrypoints** for truly different behaviors (e.g., browser vs server bindings).
- Make **contracts explicit**: if an API expects certain parameters (or must align with platform/spec behavior), encode that in types and require/normalize values rather than relying on implicit undefined handling.
- For runtime/platform differences, add **feature detection/guards** and don’t assume the same API support across engines.

Example (options bag + variant split):

```ts
type PreloadOptions = {
  integrity?: string,
  fetchPriority?: 'low' | 'auto' | 'high',
  nonce?: string,
  crossOrigin?: string,
};

// Variant-specific (avoid mode explosion)
export function preinitModuleForSSR(
  href: string,
  origin: string,
  options: PreloadOptions,
): void {
  // bindings decide final values; contract stays consistent
  const final = {
    integrity: options.integrity,
    fetchPriority: options.fetchPriority,
    nonce: options.nonce,
  };
  // ...
}
```

Apply this by reviewing any newly added parameter/behavior: if it’s the next step in an expanding positional signature or introduces a new behavioral mode, refactor toward an options object and/or a separate variant/entrypoint, and ensure the interface remains spec-accurate across supported runtimes.