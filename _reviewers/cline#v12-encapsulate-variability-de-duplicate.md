---
title: Encapsulate variability, de-duplicate
description: When improving code, favor clarity by (1) reusing existing shared/core
  utilities instead of duplicating logic in the app, (2) encapsulating behavioral
  differences behind interfaces/role objects created once (so core control-flow stays
  straight-line), (3) modeling multi-state behavior with string/discriminated unions
  rather than booleans, and (4) unifying...
repository: cline/cline#v12
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70872
---

When improving code, favor clarity by (1) reusing existing shared/core utilities instead of duplicating logic in the app, (2) encapsulating behavioral differences behind interfaces/role objects created once (so core control-flow stays straight-line), (3) modeling multi-state behavior with string/discriminated unions rather than booleans, and (4) unifying repeated formatting/escaping/wrapper construction in a single formatter parameterized by a discriminant.

How to apply
- Reuse before you rewrite: if equivalent git/shell/validation/formatting helpers already exist in core/shared, call them rather than adding new near-copies.
- Remove conditional sprawl: if you see repeated `if (outputMode === "json") ... else ...` across many sites, introduce an `outputter`/strategy created once from `outputMode`, and call the same methods on it.
- Use discriminated unions for state: prefer `"started" | "resumed"` (or similar) over `boolean resumed` so invalid combinations are hard to represent.
- Generalize formatters: if two formatters differ only by a few attributes, combine into one formatter with a discriminant that selects which attributes to include.
- Split oversized additions: if a change introduces a large amount of tool-specific code in a general module, move it into a tool-level module/file.

Example patterns
1) Replace boolean state with a string union
```ts
type ResumeMode = "start" | "resume";

type HookRuntimeOptions = {
  resumedMode?: ResumeMode;
};
```

2) Replace conditional output branching with a role/factory
```ts
interface RunOutputter {
  runStarted(...args: unknown[]): void;
  runResult(...args: unknown[]): void;
  runAborted(...args: unknown[]): void;
}

function createOutputter(outputMode: "json" | "console", verbose: boolean): RunOutputter {
  return outputMode === "json" ? new JsonRunOutputter(verbose) : new ConsoleRunOutputter(verbose);
}

// straight-line lifecycle
const outputter = createOutputter(config.outputMode, config.verbose);
outputter.runStarted(...);
// ...
outputter.runResult(...);
```

3) Generalize formatting with a discriminated union
```ts
type HookContext =
  | { kind: "tool"; source: string; toolName: string; toolCallId: string; body: string }
  | { kind: "runStart"; source: string; body: string };

function formatHookContext(ctx: HookContext): string {
  const body = ctx.body.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (ctx.kind === "tool") {
    return `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="${ctx.source}">\n${body}\n</hook_context>`;
}
```