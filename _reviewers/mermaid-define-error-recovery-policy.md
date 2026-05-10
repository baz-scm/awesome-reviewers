---
title: Define Error Recovery Policy
description: 'When handling failures, classify them as **recoverable** vs **unrecoverable**,
  then apply a consistent rule: log with enough context, **continue only for recoverable
  side-effects**, and **fail fast with explicit (prefer custom) errors** for invalid/unknown
  inputs or internal invariants.'
repository: mermaid-js/mermaid
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 87952
---

When handling failures, classify them as **recoverable** vs **unrecoverable**, then apply a consistent rule: log with enough context, **continue only for recoverable side-effects**, and **fail fast with explicit (prefer custom) errors** for invalid/unknown inputs or internal invariants.

Apply it like this:
- **Recoverable (graceful degradation):** wrap side-effect registration/optional subsystems so primary rendering still works.
- **Unrecoverable (fail fast):** unknown statement types, invalid style values, or malformed inputs should throw (don’t silently ignore).
- **Logging + propagation:** ensure default behavior remains consistent; config flags may change *how* you recover/cleanup, but should not accidentally swallow exceptions.

Example pattern (recoverable side-effect):
```ts
try {
  registerDiagramIconPacks(config.icons);
} catch (error) {
  log.error(
    'Failed to register icon packs, continuing with diagram render:',
    error,
  );
  // continue rendering
}
```

Example pattern (unrecoverable invalid input):
```ts
class InvalidStyleError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'InvalidStyleError';
  }
}

function parseRadius(value: string): number {
  if (!/^\d+$/.test(value)) {
    throw new InvalidStyleError(`radius value '${value}' must be a number`);
  }
  return parseInt(value, 10);
}
```

Example pattern (consistent propagation with suppression):
```ts
try {
  await diag.renderer.draw(text, id, version, diag);
} catch (e) {
  if (config.suppressErrorRendering) {
    removeTempElements();
  } else {
    errorRenderer.draw(text, id, version);
  }
  throw e;
}
```