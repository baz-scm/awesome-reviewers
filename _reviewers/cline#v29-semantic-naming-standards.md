---
title: Semantic Naming Standards
description: 'Use names (and types) that communicate *meaning, provenance, and correct
  usage*—especially for booleans and public APIs.


  Guidelines:

  1) Prefer semantic names over vague booleans'
repository: cline/cline#v29
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 70893
---

Use names (and types) that communicate *meaning, provenance, and correct usage*—especially for booleans and public APIs.

Guidelines:
1) Prefer semantic names over vague booleans
- If a flag is really describing a domain state, name it after that state (or use a union/enum string), rather than `background`, `isX`, or negated meanings.
- Prefer “positive” names over “not seeded”/negation.

2) Encode domain intent in types when possible
- For fields with more than one meaningful interpretation, use string unions (e.g., `entry: 'run' | 'continue'`) instead of boolean fields that hide intent.

3) Keep casing consistent with the *origin/provenance* of the value
- If callers supply keys, use the caller-side convention (e.g., camelCase).
- If keys are injected by telemetry/envelopes/global enrichment, use the enrichment convention (e.g., snake_case).
- Don’t “normalize” a single key to the other convention if that would incorrectly suggest it comes from a different source.

4) Make public API exports unambiguous
- Avoid exporting multiple similarly-shaped functions where it’s unclear which one to call.
- Prefer one canonical exported function; if multiple must exist, make names strongly indicate when each should be used and document the difference clearly.

Example pattern:
```ts
// Good: provenance + semantic state
export type EntryKind = 'run' | 'continue';
export interface Context {
  entry?: EntryKind;
}

// Good: callers supply camelCase keys; telemetry injects snake_case
function captureSdkError(context: { finishReason: string }) {
  const telemetryEnvelope = {
    // snake_case: envelope/global enrichment
    finish_reason: undefined as string | undefined,
  };

  return {
    // camelCase: caller-supplied context
    context,
    telemetryEnvelope,
  };
}

// Good: public API discoverability
// Export one primary function; keep helpers non-exported or clearly marked.
export function getEffectiveLastUsedProviderId(state: StoredProviderSettings) {
  // ...
}
```

Apply this during review whenever you touch identifiers, exported functions, or any boolean/enum-like domain fields.