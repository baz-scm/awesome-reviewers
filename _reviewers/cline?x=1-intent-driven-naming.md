---
title: Intent-Driven Naming
description: 'Use names that clearly express intent and maintain the correct meaning/contract—especially
  for externally observed identifiers.


  Rules

  - Encode domain meaning: avoid vague booleans (e.g. `background`); if the state
  has more than “true/false meaning”, use an enum/string that names the state.'
repository: cline/cline?x=1
label: Naming Conventions
language: TypeScript
comments_count: 8
repository_stars: 70861
---

Use names that clearly express intent and maintain the correct meaning/contract—especially for externally observed identifiers.

Rules
- Encode domain meaning: avoid vague booleans (e.g. `background`); if the state has more than “true/false meaning”, use an enum/string that names the state.
- Keep “name” aligned with “value/contract”: when renaming properties/headers used by consumers (telemetry events, request headers), either (a) preserve the old name/value meaning, or (b) rename the contract too and update all call sites so the new meaning is always sent.
- Follow established casing/origin conventions: for structured data, ensure naming matches the rule the system expects (e.g. keys originating from caller context vs telemetry envelope).
- Prefer discoverable public APIs: export function names should make it obvious what to call; if multiple functions differ subtly, consider exporting a single obvious “default” and/or adding highly specific docs.
- Avoid jargon in identifiers, or document it: if you use terms that aren’t universally understood, either add a clear comment explaining the intended meaning or choose clearer names.

Example (boolean -> explicit state)
```ts
// Avoid:
function load(refresh: boolean, background = false) { /* ... */ }

// Prefer:
type LoadInitiator = "userInitiated" | "systemBackground";
function load(refresh: boolean, initiator: LoadInitiator = "userInitiated") {
  if (initiator === "userInitiated") {
    // show spinner / trigger user-dependent behavior
  }
}
```

Checklist
- Does the identifier convey intent without reading implementation?
- Is the identifier’s meaning consistent with any external contract (events/headers/storage keys)?
- If you rename something, do you rename the contract and update all call sites (not relying on positional arguments)?
- Are casing/formatting conventions followed based on the data’s origin?
- Are exports easy to choose correctly, and are domain terms understandable? 