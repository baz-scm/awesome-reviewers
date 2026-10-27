---
title: Schema-driven Options Contracts
description: When designing or changing an API surface, explicitly define the input
  contract as a schema-aligned options object, make option forwarding type-required
  at boundaries, and ensure observable semantics match the underlying spec.
repository: facebook/react#b6
label: API
language: JavaScript
comments_count: 5
repository_stars: 251888
---

When designing or changing an API surface, explicitly define the input contract as a schema-aligned options object, make option forwarding type-required at boundaries, and ensure observable semantics match the underlying spec.

Practical rules:
- Prefer an options bag (object) over adding more positional/optional parameters. When an external system (e.g., tool/mcp layer) expects a keyed-arguments object, match that shape.
- At public→internal boundaries, require (via types) the complete options contract so internal dispatcher calls can’t accidentally drop fields.
- For APIs with spec-defined semantics (especially identity/keys), implement the identity tuple exactly as specified and add tests that lock in add/remove behavior.
- If an API supports extended parameters only in some environments, guard the parameter usage (feature detect / polyfill) instead of always passing unsupported objects.

Example (options contract + required forwarding):
```js
// Public API
export function preloadModule(href, options?: PreloadModuleOptions) {
  // options is user-facing; normalize/default here as needed
  const normalized = normalizePreloadModuleOptions(options);
  return preloadModuleImpl(href, normalized); // internal call expects full shape
}

// Internal dispatcher API: require the full options shape
function preloadModuleImpl(href, options: Required<PreloadModuleImplOptions>) {
  // forward all options fields explicitly
}
```

Example (spec-based identity in observable behavior):
- Implement listener identity using only `(type, callback, capture)` and treat `{passive}` changes as no-ops for the same `(type, callback, capture)` pair; cover both add and remove paths with tests.