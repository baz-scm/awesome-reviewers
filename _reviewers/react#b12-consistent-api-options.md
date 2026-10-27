---
title: Consistent API Options
description: 'When designing or evolving APIs (including internal-but-consumed tooling
  surfaces and DOM/SSR helper APIs), make the contract explicit and consistent:'
repository: facebook/react#b12
label: API
language: JavaScript
comments_count: 5
repository_stars: 251896
---

When designing or evolving APIs (including internal-but-consumed tooling surfaces and DOM/SSR helper APIs), make the contract explicit and consistent:

- **Use consistent entrypoints/bindings intentionally.** If browser and server behavior differs, encode it in the package surface (separate entrypoints) rather than relying on implicit runtime branching.
- **Prefer an options bag for extensible configuration.** If you’re adding optional behavior (e.g., `includeHooks`), consider `options` as a single argument to avoid positional-parameter churn and to match any existing public schema expectations.
- **Make required configuration explicit in the function signature/types.** If a helper like `preinitModuleForSSR` semantically depends on fields (e.g., `integrity`, `fetchPriority`), ensure the binding layer doesn’t silently omit them—pass values via the signature so behavior is predictable.
- **Canonicalize inputs/identity to match the spec.** When an API’s behavior depends on “identity” (event listener identity tuples, preload type strings, etc.), encode the correct key/semantic values in one place and add tests to prevent regressions.

Example pattern (options bag + explicit fields):
```js
function preinitModuleForSSR(href, {
  integrity,
  fetchPriority,
  nonce,
  crossOrigin,
} /* required semantically */) {
  // Always set or intentionally derive these fields in one spot.
}

function callSite(props) {
  preinitModuleForSSR(props.href, {
    integrity: props.integrity ?? undefined,
    fetchPriority: props.fetchPriority ?? undefined,
    nonce: props.nonce,
    crossOrigin: props.crossOrigin,
  });
}
```

If you follow these rules, API consumers get stable, predictable behavior across environments, and you reduce “mystery omissions” (missing fields) and semantic drift (incorrect standardized values or identity keys).