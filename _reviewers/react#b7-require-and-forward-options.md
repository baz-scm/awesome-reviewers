---
title: Require and Forward Options
description: When designing/adding API parameters for cross-layer calls (public API
  → dispatcher/bindings → internal tooling), use an explicit options shape and make
  behavior-changing fields required so they can’t be accidentally dropped.
repository: facebook/react#b7
label: API
language: JavaScript
comments_count: 4
repository_stars: 251888
---

When designing/adding API parameters for cross-layer calls (public API → dispatcher/bindings → internal tooling), use an explicit options shape and make behavior-changing fields required so they can’t be accidentally dropped.

**Rules**
- Prefer an **options bag / keyed arguments object** over adding new positional parameters (especially for extensibility and tooling schemas).
- If an option value affects network/resource behavior (e.g., `integrity`, `nonce`, `fetchPriority`, etc.), ensure the “bridge/dispatcher” layer **requires** it (or explicitly defines defaults), rather than accepting a loosely typed/nullable options object and then selectively forwarding.
- For public interfaces, align with any tool input schema expectations: the input should be an object with named keys (not an argument list whose meaning depends on call patterns).

**Example (signature shape + forwarding enforcement)**
```js
// Prefer an options bag for extensibility
function preloadModule(href, {
  integrity,
  nonce,
  fetchPriority,
  crossOrigin,
} /* required keys or explicitly defaulted */) {
  // Forward all keys intentionally
  return dispatcher.preloadModule(href, {
    integrity,
    nonce,
    fetchPriority,
    crossOrigin,
  });
}

// If you must accept an options object, don’t allow “silently missing required forwarding”
// at the dispatcher boundary—require the needed fields or define defaults there.
```

Applying this will prevent subtle divergences where one binding forgets to forward a field, and will make API evolution (new fields/behavior) safer and easier to validate.