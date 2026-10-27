---
title: Explicit API Contracts
description: 'When designing/altering public-facing APIs, make misuse hard by (1)
  enforcing valid context and (2) making required option contracts explicit.


  Apply this standard:'
repository: facebook/react#b15
label: API
language: JavaScript
comments_count: 4
repository_stars: 251891
---

When designing/altering public-facing APIs, make misuse hard by (1) enforcing valid context and (2) making required option contracts explicit.

Apply this standard:
- Prevent invalid context usage: if an API is server-only, don’t export it for client bundles in a way that silently “does nothing”; instead, make it un-importable or fail immediately with a clear error.
- Require boundary options: for functions that must forward options to lower layers, ensure the boundary signature requires the complete option shape (so “forgot to forward X” can’t compile or slip through reviews).
- Keep interface shapes schema-friendly: for tooling/public interfaces, prefer an options bag (or otherwise schema-mapped argument object) over positional optional params, so the externally documented contract matches what the schema expects.

Examples (patterns)
- Server-only API gating:
  - Prefer not exporting client-callable entry points; if you must keep an export, throw in client context rather than returning a no-op.
- Required option forwarding:
  - Change signatures so options are required at the boundary, e.g.:
    ```js
    // Before: optional/nullable options can be dropped accidentally
    function preloadModuleImpl(href, options?: ?PreloadModuleImplOptions) { ... }

    // After: require the full option contract when the public API expects it
    function preloadModuleImpl(href, options?: Required<PreloadModuleImplOptions>) { ... }
    ```
- Schema-friendly tooling args:
  - Use a single argument object/options bag with keys that match the public tool schema.

Result: clearer contracts, earlier errors, and fewer “works in some environments / missing option forwarding” bugs.