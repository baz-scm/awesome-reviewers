---
title: Prefer shared abstractions
description: 'Adopt a “single source of truth” style: avoid duplicating logic, centralize
  shared helpers, and replace scattered conditionals with explicit abstractions.'
repository: cline/cline#v28
label: Code Style
language: TypeScript
comments_count: 8
repository_stars: 70892
---

Adopt a “single source of truth” style: avoid duplicating logic, centralize shared helpers, and replace scattered conditionals with explicit abstractions.

Apply these rules:
1) Reuse existing shared logic
- If there’s already a helper/module for the same behavior (e.g., remote/refs normalization, shell detection), import and use it instead of re-implementing.

2) Don’t keep near-duplicate implementations
- When two functions share the same escaping/trimming/wrapping rules or lifecycle semantics, generalize them into one formatter/function using a discriminated union (tool vs run-start) or a role/interface (console vs JSON output).

3) Replace “if outputMode === …” threading with a role/factory
- Create one outputter at startup and call lifecycle methods (e.g., `runStarted`, `runResult`) through a common interface; only the factory should branch on mode.
- Keep concerns orthogonal in the types/flow (e.g., `verbose` should affect both outputters consistently).

4) Model state with unions, not booleans
- For session/run behavior that has multiple meaningful states (e.g., resumed vs not), use a string union (or enum) so invalid combinations don’t silently slip in.

5) Maintainability hygiene
- Extract magic numbers into named constants (especially timeouts/fallback delays).
- Remove stale/unneeded imports after refactors.
- Split large tool-specific blocks into dedicated modules to keep files focused.

Example (role-based output instead of scattered conditionals):
```ts
type RunOutputter = {
  runStarted(): void;
  runResult(result: unknown): void;
};

function createRunOutputter(mode: "json" | "console", verbose: boolean): RunOutputter {
  return mode === "json" ? new JsonRunOutputter(verbose) : new ConsoleRunOutputter(verbose);
}

export async function runAgent(...) {
  const outputter = createRunOutputter(config.outputMode, config.verbose);
  outputter.runStarted();
  // straight-line lifecycle calls; no repeated if/else throughout
}
```