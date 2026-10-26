---
title: Prefer shared roles and unions
description: 'When implementing behavior that varies by mode/state, avoid duplicating
  existing logic and avoid scattering conditional branches. Instead:


  1) Reuse shared utilities'
repository: cline/cline#v11
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70871
---

When implementing behavior that varies by mode/state, avoid duplicating existing logic and avoid scattering conditional branches. Instead:

1) Reuse shared utilities
- Before adding a parallel implementation (git runner, shell detection, context formatter), search for an existing helper in core/shared and call it.
- If the app needs snapshot/special logic, move the shared part into core next to the existing preflight/formatters instead of keeping a second “runner/formatter” in the app.

2) Replace mode conditionals with role/strategy objects
- If code has repeated `if (outputMode === "json") ... else ...` paths, create a `RunOutputter` (or similar) once at startup via a factory, and route events via straight-line calls.
- Keep orthogonal concerns (e.g., verbosity vs output format) flowing through all outputters via parameters, rather than relying on nested conditionals.

3) Use discriminated unions for multi-state options
- Don’t use booleans to represent multiple valid states. Prefer a string union (e.g., `"start" | "resume" | "unknown"`) so invalid combinations can’t arise and testing becomes straightforward.

Example pattern (role factory + straight-line lifecycle calls):
```ts
type OutputMode = "json" | "console";

type RunOutputter = {
  runStarted(): void;
  runResult(result: unknown): void;
  runAborted(reason: unknown): void;
};

function createRunOutputter(mode: OutputMode, verbose: boolean): RunOutputter {
  return mode === "json"
    ? { runStarted: () => {/* emit json start */}, runResult: () => {/* ... */}, runAborted: () => {/* ... */} }
    : { runStarted: () => {/* write to console */}, runResult: () => {/* ... */}, runAborted: () => {/* ... */} };
}

export async function runAgent(/* ... */ config: { outputMode: OutputMode; verbose: boolean }) {
  const out = createRunOutputter(config.outputMode, config.verbose);
  out.runStarted();
  try {
    const result = await /* ... */;
    out.runResult(result);
  } catch (e) {
    out.runAborted(e);
    throw e;
  }
}
```

Applying this consistently will reduce duplicate logic, make behavior changes easier (add/modify a role or union member), and improve readability/maintainability.