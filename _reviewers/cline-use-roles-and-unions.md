---
title: Use roles and unions
description: When code has multiple behavioral variants (output format, hook context
  type, session state), prefer modeling the variation explicitly with types/roles
  and reusing shared logic—rather than duplicating implementations or threading many
  conditionals/flags.
repository: CLINE/cline
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70839
---

When code has multiple behavioral variants (output format, hook context type, session state), prefer modeling the variation explicitly with types/roles and reusing shared logic—rather than duplicating implementations or threading many conditionals/flags.

Apply these rules:
- Avoid duplicate “runner/normalizer/formatter” logic: reuse the existing core implementation (or move the logic to the shared layer once, not in multiple places).
- Replace conditional sprawl with a role/interface chosen once (factory at the entry point). Keep lifecycle calls straight-line.
- Prefer discriminated unions / string unions over booleans for state. Booleans tend to grow into confusing combinations.
- Keep modules cohesive: split large, tool-specific additions into dedicated modules.
- Keep imports minimal after refactors.

Example pattern (roles + straight-line lifecycle):
```ts
type OutputMode = "json" | "console";

type RunOutputter = {
  runStarted(): void;
  runResult(result: unknown): void;
  runAborted(reason: unknown): void;
  verbose: boolean;
};

function createRunOutputter(mode: OutputMode, verbose: boolean): RunOutputter {
  if (mode === "json") return new JsonRunOutputter({ verbose });
  return new ConsoleRunOutputter({ verbose });
}

export async function runAgent(/*...*/ config: { outputMode: OutputMode; verbose: boolean }) {
  const outputter = createRunOutputter(config.outputMode, config.verbose);
  outputter.runStarted();
  try {
    const result = await doRun();
    outputter.runResult(result);
  } catch (e) {
    outputter.runAborted(e);
  }
}
```

Example pattern (union instead of boolean):
```ts
type ResumeState = "none" | "resumed";

type HookRuntimeOptions = {
  resumed?: ResumeState; // better than boolean
};
``` 

Checklist: if you’re seeing repeated formatting wrappers, copied normalization code, nested `if (outputMode === "json") ...` branches, or `*?: boolean` options representing more than two real states—refactor toward shared utilities, role-based dispatch, and discriminated unions.