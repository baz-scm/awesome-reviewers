---
title: Environment-Safe API Surfaces
description: APIs that differ by runtime (e.g., server-only vs browser/client) should
  be represented explicitly in the public surface. Avoid “shared” exports that can
  be imported in the wrong environment, and avoid letting variant behavior accumulate
  into ever-growing positional parameter lists.
repository: facebook/react#b13
label: API
language: JavaScript
comments_count: 3
repository_stars: 251894
---

APIs that differ by runtime (e.g., server-only vs browser/client) should be represented explicitly in the public surface. Avoid “shared” exports that can be imported in the wrong environment, and avoid letting variant behavior accumulate into ever-growing positional parameter lists.

Apply this as follows:
1) Split client vs server entrypoints
- If an implementation decision (or bundling strategy) differs by environment, expose separate entrypoints so the correct code (and types) are selected automatically.

2) Fail fast for server-only imports
- Do not export server-only helpers into client-safe modules as silent no-ops.
- Instead, make incorrect usage error early (ideally at import/initialization time), so mistakes surface during development.

3) For variant-heavy APIs, split by variant (or use structured options)
- When behavior depends on many “mode” inputs, don’t expand positional args indefinitely.
- Prefer separate functions per variant (or a single typed options object that models the variant), so downstream code can inline/optimize without ambiguity.

Example pattern:
```js
// client entrypoint: client.js
export { resolveServerReference } from './ReactFlightClientConfigBundlerFB.client';
// server-only entrypoint: server.js
export { createMaskLedger, addToLedger } from './ledger.server';

// server-only module (ledger.server.js)
throw new Error('createMaskLedger/addToLedger are server-only; import from server entrypoint');
```

Team standard takeaway: keep the API shape “correct by construction” for each runtime/variant, and make invalid cross-environment usage obvious rather than silently tolerated.