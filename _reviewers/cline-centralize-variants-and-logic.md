---
title: Centralize Variants and Logic
description: When code introduces multiple “modes” (output modes, session start vs
  resume, tool vs run-start context) or repeats non-trivial logic (git checks, shell
  detection, escaping/formatting), prefer explicit variant modeling and centralized
  utilities rather than duplicating logic or branching everywhere.
repository: ClInE/cLiNe
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70838
---

When code introduces multiple “modes” (output modes, session start vs resume, tool vs run-start context) or repeats non-trivial logic (git checks, shell detection, escaping/formatting), prefer explicit variant modeling and centralized utilities rather than duplicating logic or branching everywhere.

Guidelines
- Replace repeated `if (outputMode === ...)` threading with a single strategy/role object created once (e.g., `RunOutputter`). Lifecycle calls should be straight-line; each outputter decides what to emit.
- Model multi-state concepts with discriminated unions / string unions instead of booleans. This prevents invalid combinations and improves readability and testability.
- Don’t re-implement existing checks/helpers; reuse shared functions from `core` / `@cline/shared`. If logic belongs at the platform level, move it to `core` near the existing “preflight”/shared implementation and keep app code thin.
- Avoid duplicating formatting/escaping rules. Use one generalized formatter with a discriminated union input (tool-context vs run-start-context) so escaping/wrapping happens in one place.
- Keep code hygiene tight: remove unused imports and redundant local helpers when shared ones exist.

Example (strategy + discriminated union)
```ts
type SessionKind =
  | { kind: "start" }
  | { kind: "resume" };

type RunOutputter = {
  runStarted(): void;
  runResult(result: unknown): void;
  runAborted(err: unknown): void;
};

function createOutputter(outputMode: "json" | "console", verbose: boolean): RunOutputter {
  return outputMode === "json"
    ? new JsonRunOutputter({ verbose })
    : new ConsoleRunOutputter({ verbose });
}

async function runAgent(session: SessionKind) {
  const outputter = createOutputter("json", /* verbose */ false);

  if (session.kind === "resume") {
    // dispatch agent_resume
  } else {
    // dispatch agent_start
  }

  outputter.runStarted();
  // ... straight-line lifecycle calls
}
```

Applying this consistently yields code that is easier to read, easier to extend, and less prone to subtle drift between duplicated implementations.