---
title: Explicit API Contracts
description: All externally observable behaviors and data shapes must follow the API
  contract exactly, and request/behavior parameters should be explicit and self-documenting.
repository: cline/cline#v6
label: API
language: TypeScript
comments_count: 3
repository_stars: 70864
---

All externally observable behaviors and data shapes must follow the API contract exactly, and request/behavior parameters should be explicit and self-documenting.

**Standards**
1. **No contract exceptions**: If a spec defines what an API MUST/ MUST NOT return (e.g., tool visibility), do not gate compliance behind unrelated feature flags. Keep filtering/selection logic aligned with the contract.
2. **End-to-end field propagation**: When adding a request/command/event field, ensure it is carried through *every* projection/conversion layer so the field does not become “input-only.” Add regression tests that compare payloads at each boundary.
3. **Prefer named options over boolean flags**: Public functions that change behavior should use an options object with named fields (and defaults via destructuring), not positional booleans.

**Example: replace booleans with an options object**
```ts
// Before (ambiguous)
load(refresh: boolean, background: boolean)

// After (explicit)
type LoadOptions = { refresh?: boolean; background?: boolean };

function load(options: LoadOptions = {}) {
  const { refresh = false, background = false } = options;
  // ...
}
```

**Checklist when modifying an API**
- Does the output still satisfy all MUST/MUST NOT rules (no hidden exceptions)?
- If you added/changed a field, is it forwarded through all event copies / handlers / adapters?
- Are behavior toggles represented as `options` with named fields (no boolean ambiguity)?