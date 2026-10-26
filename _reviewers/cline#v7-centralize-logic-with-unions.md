---
title: Centralize logic with unions
description: 'When adding or updating code, avoid duplicating existing logic and avoid
  “configuration branching” spread across the codebase.


  **Apply this standard:**'
repository: cline/cline#v7
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70865
---

When adding or updating code, avoid duplicating existing logic and avoid “configuration branching” spread across the codebase.

**Apply this standard:**
1. **Reuse existing shared implementations**: if core/shared packages already normalize/validate/format/check something, call that instead of creating app-local “snapshot” logic.
2. **Centralize behavior selection**: if behavior depends on mode/state, choose the behavior once using a **role/interface + factory** (or an equivalent initialization step), rather than threading `if (outputMode === ...)` through many call sites.
3. **Use expressive types for state**: prefer **string unions/discriminated unions** over booleans so states are explicit and invalid combinations are hard to represent.
4. **Keep formatting/escaping rules in one place**: for repeated transformations (e.g., trimming + escaping + wrapper tags), use a single formatter that varies only the emitted attributes via a discriminated union.

**Example pattern (role/factory to remove scattered branching):**
```ts
type OutputMode = "json" | "console";

interface RunOutputter {
  runStarted(): void;
  runResult(result: unknown): void;
}

class JsonRunOutputter implements RunOutputter {
  constructor(private verbose: boolean) {}
  runStarted() {}
  runResult(_: unknown) {}
}

class ConsoleRunOutputter implements RunOutputter {
  constructor(private verbose: boolean) {}
  runStarted() {}
  runResult(_: unknown) {}
}

function makeRunOutputter(mode: OutputMode, verbose: boolean): RunOutputter {
  return mode === "json" ? new JsonRunOutputter(verbose) : new ConsoleRunOutputter(verbose);
}
```

**Result:** clearer intent, fewer conditionals, less duplicated code, and easier maintenance/testing.