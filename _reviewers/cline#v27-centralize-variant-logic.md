---
title: Centralize variant logic
description: 'When code behavior varies by “mode/state” or platform/tool type, avoid
  scattered `if/else` branches and duplicated helper/formatter implementations. Instead:'
repository: cline/cline#v27
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70892
---

When code behavior varies by “mode/state” or platform/tool type, avoid scattered `if/else` branches and duplicated helper/formatter implementations. Instead:

- Centralize shared logic in the most appropriate shared/core module and reuse existing helpers.
- Model variants explicitly with discriminated unions (or string unions) and/or strategy/role interfaces.
- Keep formatting/escaping/normalization rules in one place (generalize the formatter rather than adding parallel formatters).
- Extract large, tool-specific behavior into a dedicated module to keep concerns separated.

Example (strategy for output + explicit variant state):
```ts
type Outputter = {
  runStarted(ctx: unknown): void;
  runResult(result: unknown): void;
  runAborted(err: unknown): void;
};

type ResumeState = { type: "start" } | { type: "resume" };

function makeOutputter(outputMode: "json" | "console", verbose: boolean): Outputter {
  return outputMode === "json"
    ? new JsonRunOutputter({ verbose })
    : new ConsoleRunOutputter({ verbose });
}

function dispatchRunStarted(outputter: Outputter, resume: ResumeState, ctx: unknown) {
  // Straight-line calls; no mode threading through the rest of the code.
  outputter.runStarted({ ...ctx, resumed: resume.type === "resume" });
}
```

Applying this standard reduces copy/paste drift (git/shell/formatter logic), clarifies which states are valid, and makes future changes (new output modes, new hook/run layers, new tools) localized and testable.