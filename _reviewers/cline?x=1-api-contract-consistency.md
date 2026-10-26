---
title: API Contract Consistency
description: When designing or evolving APIs, treat the contract as a single source
  of truth and ensure request/response behavior is consistent, unambiguous, and spec-compliant.
repository: cline/cline?x=1
label: API
language: TypeScript
comments_count: 5
repository_stars: 70861
---

When designing or evolving APIs, treat the contract as a single source of truth and ensure request/response behavior is consistent, unambiguous, and spec-compliant.

Apply these rules:
1) Follow the spec/contract unconditionally
- Don’t gate required behavior behind feature flags unless the spec explicitly allows it.

2) Round-trip new fields end-to-end
- If you add a request field (e.g., displayPrompt), every projection/event copy that receives it must forward it onward; missing propagation creates “field in, field lost” bugs.

3) Use named options objects instead of boolean parameters
- Boolean flags make call sites unclear and easy to mix up.

4) Avoid duplicated “readiness”/capability flags
- Don’t mirror shared provider catalog readiness in UI/session config. Derive optionality/capabilities from the shared contract metadata instead.

5) Make endpoint versioning robust
- Normalize base URLs (strip trailing slashes, remove an optional version prefix) before appending the correct versioned route.

Example (options object vs booleans + forward new fields):
```ts
// Prefer options object over booleans
function load(opts: { refresh?: boolean; background?: boolean } = {}) {
  const { refresh = false, background = false } = opts;
  if (refresh && !background) showSpinner();
  return doFetch({ refresh, background });
}

// Ensure new fields round-trip through event/projection copies
type Input = { prompt: string; displayPrompt?: string };
type Event = { prompt: string; displayPrompt?: string };

function projectPendingPrompt(input: Input): Event {
  return {
    prompt: input.prompt,
    displayPrompt: input.displayPrompt, // forward it
  };
}
```

When updating API behavior, add/adjust tests specifically for:
- Visibility/spec compliance edge cases
- Missing-field propagation (field present in one payload, absent in the other)
- Endpoint normalization across trailing slashes and pre-versioned base URLs
- Correct interpretation of named options at call sites