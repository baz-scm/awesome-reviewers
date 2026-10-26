---
title: Intention-Revealing Naming
description: 'Adopt a naming standard where identifiers reflect meaning and lifecycle
  boundaries, and where casing/values stay consistent with their source.


  **Rules**'
repository: cline/cline#v13
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70874
---

Adopt a naming standard where identifiers reflect meaning and lifecycle boundaries, and where casing/values stay consistent with their source.

**Rules**
1. **Prefer semantic state over booleans**: if the situation has more than two meaningful cases (or the “other” case is unclear), use a descriptive string/enum instead of `boolean`.
2. **Avoid vague names**: parameters like `background` should be renamed to what the flag *actually* represents (e.g., `userInitiated`).
3. **Encode lifecycle boundaries in stable ids**: when an id drives UI state/highlights, ensure it stays stable across the intended scope (e.g., “the whole turn”) and only changes when the consumer must refresh.
4. **Standardize shared identifiers**: use shared union/types (e.g., `ClientName`) rather than ad-hoc string literals so callers and downstream systems agree.
5. **Keep naming/casing consistent with origin**: for telemetry keys, apply casing rules based on where the data originates (caller context vs telemetry envelope/global enrichment).
6. **Renames must preserve semantics**: if you rename a parameter/property because the meaning changes, update all positional call sites (and audit related helpers). When possible, use object parameters to make mismatches harder to compile silently.
7. **Public API names must be obvious**: export one “intended default” entrypoint or use names that clearly tell callers which function to pick.

**Example (state instead of boolean)**
```ts
type Entry = 'run' | 'continue' | undefined;
type PromptSeed = 'seeded' | 'written' | undefined;

function describeRun(entry?: Entry, promptSeed?: PromptSeed) {
  // Names tell you what happened; no negation required.
}
```