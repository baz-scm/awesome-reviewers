---
title: Semantic, Consistent Naming
description: Use naming that communicates meaning, follows established casing/provenance
  rules, stays consistent across shared types and call sites, and makes the correct
  API choice obvious.
repository: CLINE/CLINE
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 70837
---

Use naming that communicates meaning, follows established casing/provenance rules, stays consistent across shared types and call sites, and makes the correct API choice obvious.

Apply these rules:

- Prefer intent/state names over vague booleans
  - Good: `userInitiated` instead of `background`.
- Avoid boolean fields when the domain state needs explanation; model it as a positive, descriptive set of values
  - Prefer string-literal unions (or enums) that say what the state *is*.
- Standardize on shared identifier types across modules
  - If a shared type exists (e.g., `ClientName`), don’t reintroduce parallel “client” names that drift.
- When renaming identifiers/keys (especially telemetry), update every call site and keep event-property keys consistent
  - Positional renames can typecheck while silently breaking downstream joins.
- Make exported/public APIs easy to choose
  - Prefer one exported “main” function; if multiple are public, ensure names strongly indicate which one callers should use.
- Follow existing casing conventions based on provenance
  - Example rule: keys provided by callers in a `context` object are camelCase; keys added by telemetry envelopes/global enrichment are snake_case.

Example:
```ts
// Prefer descriptive state over ambiguous booleans
type Entry = "run" | "continue";
type PromptState = "seeded" | "written";

interface AgentRunLifecycleContext {
  entry?: Entry;
  promptState?: PromptState;
}

// Prefer shared identifiers
type ClientName = "cline-cli" | "cline-desktop" | "cline-vscode" | "cline-jetbrains";

function buildRequest(client: ClientName) {
  // ...
}
```

If a name change affects identifiers/keys, treat it like a breaking change: rename + update all producers/consumers together, then add/verify tests that assert the emitted keys.