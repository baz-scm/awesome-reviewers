---
title: Centralize shared API logic
description: When building request/response transformation, endpoint resolution, or
  validation logic that must behave identically across multiple provider formats,
  client types, or entry points (e.g. live execution vs. a "test connection" probe),
  implement it once in a shared module and have every consumer import and call that
  single implementation. Never duplicate the...
repository: decolua/9router?probeA1
label: API
language: JavaScript
comments_count: 3
repository_stars: 31730
---

When building request/response transformation, endpoint resolution, or validation logic that must behave identically across multiple provider formats, client types, or entry points (e.g. live execution vs. a "test connection" probe), implement it once in a shared module and have every consumer import and call that single implementation. Never duplicate the same rule in parallel code paths — divergent copies drift silently and produce real bugs: a tool-call interception that only ran in the non-streaming handler let forced-streaming providers leak an unhandled tool call to the client, and duplicated JSON-repair logic across two provider translators risked going out of sync. Similarly, endpoint URL construction and "is this response valid" status-code rules for Azure were centralized into `resolveAzureTarget` and `isAzureProbeValid` so the "Test" button and the actual executor can never disagree about what endpoint or status is acceptable.

Checklist when adding behavior that spans multiple formats/clients/entry points:
- Identify every code path that needs the same rule (all provider translators, all client response formats, both the live executor and its validation/test route).
- Extract the rule into one exported function/module (e.g. `toolArgs.js`, `resolveAzureTarget`), not a copy per path.
- Apply it at every relevant integration/return point, guarding it internally so it is a no-op when not applicable.
- Add regression tests that exercise each format/client/path combination to prevent future gaps.

Example pattern:
```js
// shared module, single source of truth
export function resolveAzureTarget(psd, model) { /* one set of URL rules */ }
export function isAzureProbeValid(status, responses) { /* one set of status rules */ }

// used identically by the executor and the validate/test route
const { url } = resolveAzureTarget(psd, model);
const ok = isAzureProbeValid(response.status, responses);
```