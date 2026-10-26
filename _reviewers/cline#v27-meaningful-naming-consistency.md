---
title: Meaningful Naming Consistency
description: Adopt naming that is (1) semantically precise, (2) consistent with existing
  shared types/conventions, and (3) unambiguous to callers—especially for identifiers
  and public APIs.
repository: cline/cline#v27
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70892
---

Adopt naming that is (1) semantically precise, (2) consistent with existing shared types/conventions, and (3) unambiguous to callers—especially for identifiers and public APIs.

Practical rules:
- Prefer shared “source of truth” identifier types (e.g., client/host names) rather than ad-hoc string unions.
- Avoid vague boolean/negative flags. If a value represents a domain state, model it as descriptive string states (positive/explicit) instead of booleans and `!flag` logic.
- Ensure public/exported function names make it obvious which one callers should use; if there are multiple related entry points, either (a) export one primary function or (b) use names + docs that precisely explain when each is correct.
- Keep naming conventions tied to the key’s origin. For example, if keys come from the caller’s `context`, use caller-style casing; if they’re added by the telemetry envelope/global enrichment, use the envelope’s casing.
- Treat renaming of identifier properties as a format change: update all call sites and ensure the new property name matches the actual value being sent (so the same telemetry key never contains different identifier formats).
- Don’t rely on internal jargon for exported/module-level intent; either document the terminology at the file level or choose clearer words.

Example (replace vague boolean with explicit state):
```ts
// Before: ambiguous
async function load(refresh: boolean, background = false) {
  if (!background) { /* ... */ }
}

// After: explicit and positive
type LoadInitiation = "userInitiated" | "programmatic";
async function load(refresh: boolean, initiation: LoadInitiation = "userInitiated") {
  if (initiation === "userInitiated") { /* ... */ }
}
```