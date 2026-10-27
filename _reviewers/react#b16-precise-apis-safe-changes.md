---
title: Precise APIs, Safe Changes
description: 'When changing or extending any externally observable surface (options,
  entrypoints, callable APIs, or modeled function signatures), do three things:


  1) Model the real contract precisely'
repository: facebook/react#b16
label: API
language: TypeScript
comments_count: 3
repository_stars: 251891
---

When changing or extending any externally observable surface (options, entrypoints, callable APIs, or modeled function signatures), do three things:

1) Model the real contract precisely
- Ensure the function/options signature you encode matches the actual call form and parameter effects/semantics.
- Example pattern (modeled signature/effects):
  - If the function is `with(index, value)`, encode it as
    - `positionalParams: [Effect.Read, Effect.Capture]`

2) Prefer deprecation over removal
- For public or user-facing options/flags, deprecate instead of deleting unless you can confidently classify it as a breaking change and have clear documentation/communication.

3) Keep interfaces minimal and avoid redundant context plumbing
- If a callee already has access to required context (e.g., via its owning object/environment), don’t expand its API by passing the same context again.
- This reduces coupling and prevents inconsistent sources of truth.

Applying this standard makes API changes safer, behavior easier to reason about, and internal boundaries cleaner.