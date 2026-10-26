---
title: Null and Context Safety
description: 'Treat `null`/`undefined`/empty values and “missing context” as first-class
  states: normalize inputs at boundaries, encode conditional presence in types, and
  avoid silent behavioral fallbacks when required context is absent.'
repository: cline/cline#v8
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 70867
---

Treat `null`/`undefined`/empty values and “missing context” as first-class states: normalize inputs at boundaries, encode conditional presence in types, and avoid silent behavioral fallbacks when required context is absent.

Practical rules:
1) Normalize external `null` early
- If schemas or downstream logic expect `string`, convert model-provided `null` to “field omitted” (or a safe default) before using it.

2) Distinguish `undefined` from empty collections
- When retry/optional payload fields can be omitted vs explicitly sent as `[]`, preserve that distinction. Don’t use `||`/truthy checks that collapse these cases.

3) Encode “field only exists in some lifecycle states” in TypeScript
- Prefer discriminated unions (or mapped types) so compile-time checks enforce “only set for beforeRun” rather than runtime `undefined` branching.

4) Remove nullable/optional invariants where possible
- Initialize fields in the constructor so functions don’t need `?`/extra conditionals; make “once started, always present” a type-level guarantee.

5) Don’t silently degrade UX/behavior on missing facts
- If logic depends on matching context (e.g., provider auth vs providerId), handle “unknown/mismatched” explicitly rather than falling back to an unrelated action/message.

Example (null normalization + type-safe branching):
```ts
// 1) Normalize null -> omission at runtime (before using the value)
const normalized = input.old_text === null ? undefined : input.old_text;

// 2) Type-safe conditional presence via union
type Lifecycle =
  | { kind: "beforeRun"; entry: "run" | "continue"; /* beforeRun-only fields */ }
  | { kind: "afterRun"; /* afterRun fields */ };

function handle(l: Lifecycle) {
  if (l.kind === "beforeRun") {
    // entry is guaranteed here
    useEntry(l.entry);
  }
}
```

Apply this checklist whenever you touch: auth/credential resolution, cloud/local routing, schema validation boundaries, retry payloads, and lifecycle/diagnostic event classification.