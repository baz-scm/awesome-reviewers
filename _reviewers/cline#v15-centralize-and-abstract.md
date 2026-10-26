---
title: Centralize and Abstract
description: 'Prefer centralizing shared logic and abstracting behavior instead of
  duplicating implementations or scattering conditionals.


  Do:

  - Reuse existing core/shared helpers whenever the logic already exists (git preflight,
  shell detection, message/title inference, escaping/formatting rules). If it’s missing,
  move it into the shared/core module rather than adding...'
repository: cline/cline#v15
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70877
---

Prefer centralizing shared logic and abstracting behavior instead of duplicating implementations or scattering conditionals.

Do:
- Reuse existing core/shared helpers whenever the logic already exists (git preflight, shell detection, message/title inference, escaping/formatting rules). If it’s missing, move it into the shared/core module rather than adding a parallel app-specific copy.
- Replace repeated branching (e.g., output-mode conditionals) with a single strategy/role object created once at startup, so lifecycle calls are straight-line and consistent.
- Model multi-state concepts with discriminated unions / string unions instead of booleans, to prevent invalid combinations and make intent explicit.
- Generalize duplicated “formatter” logic by using a discriminated union (one escaping/trimming/wrapping path, varying only the tool-specific fields).

Don’t:
- Add local helper functions that only replicate what a shared utility already provides.
- Add parallel formatters/utility code paths that drift over time.

Example (pattern):
```ts
// 1) Strategy/role to avoid scattered if/else
type RunOutputter = {
  runStarted(): void;
  runResult(result: unknown): void;
};

function makeOutputter(outputMode: "json" | "console", verbose: boolean): RunOutputter {
  return outputMode === "json"
    ? new JsonRunOutputter({ verbose })
    : new ConsoleRunOutputter({ verbose });
}

// 2) String union instead of boolean
type AgentResumeState = "start" | "resume";

function dispatchRunStart(state: AgentResumeState) {
  return state === "resume" ? "agent_resume" : "agent_start";
}

// 3) One formatter via discriminated union
type HookContext =
  | { kind: "tool"; source: string; toolName: string; toolCallId: string; body: string }
  | { kind: "runStart"; source: string; body: string };

function formatHookContextBlock(ctx: HookContext) {
  const body = ctx.body.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  return ctx.kind === "tool"
    ? `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`
    : `<hook_context source="${ctx.source}">\n${body}\n</hook_context>`;
}
```