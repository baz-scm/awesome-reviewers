---
title: Centralize and Compose Logic
description: 'Prefer shared, centralized helpers and “role” objects over duplicated
  local implementations and scattered conditionals.


  **Rules**

  - **Avoid duplicated logic:** If the same behavior already exists in `@cline/core`
  (e.g., git normalization/preflight, shell detection, message escaping/formatting),
  reuse it or move the new logic into the shared module near the...'
repository: cline/cline#v1
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70862
---

Prefer shared, centralized helpers and “role” objects over duplicated local implementations and scattered conditionals.

**Rules**
- **Avoid duplicated logic:** If the same behavior already exists in `@cline/core` (e.g., git normalization/preflight, shell detection, message escaping/formatting), reuse it or move the new logic into the shared module near the existing implementation.
- **Centralize formatting rules:** When two formatters do the same trimming/escaping/wrapper work, consolidate into one formatter and route differences via a **discriminated union** (so escaping/neutralization stays in exactly one place).
- **Replace branching with strategies/roles:** If code repeatedly does `if (outputMode === "json") ... else ...`, create the outputter once (e.g., `JsonRunOutputter` vs `ConsoleRunOutputter`) and use straight-line calls.
- **Use unions for state, not booleans:** For fields that affect control flow, prefer a string/union type that enumerates all valid states (prevents invalid combinations and makes intent explicit).
- **Keep modules focused:** If a change becomes tool/command-specific and large, split it into a dedicated module to avoid bloated files.

**Example: outputter role (replace scattered conditionals)**
```ts
type OutputMode = "json" | "console";

type RunOutputter = {
  runStarted(): void;
  runResult(result: unknown): void;
};

function createRunOutputter(outputMode: OutputMode, verbose: boolean): RunOutputter {
  return outputMode === "json"
    ? new JsonRunOutputter({ verbose })
    : new ConsoleRunOutputter({ verbose });
}

// once, at start
const outputter = createRunOutputter(config.outputMode, config.verbose);
outputter.runStarted();
outputter.runResult(result);
```

**Example: discriminated union for formatter routing (single escaping/trim path)**
```ts
type ToolHookCtx = { kind: "tool"; toolName: string; toolCallId: string; text: string };
type RunStartCtx = { kind: "runStart"; text: string };
type HookCtx = ToolHookCtx | RunStartCtx;

function formatHookCtx(ctx: HookCtx): string {
  const body = ctx.text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (ctx.kind === "tool") {
    return `<hook_context source="${ctx.kind}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```

Applying this consistently will make code easier to read, test, and maintain—because shared behavior lives in one place, and control-flow choices are explicit and type-safe.