---
title: Centralize Logic And State
description: When code introduces behavior that’s already implemented elsewhere (utils/formatters/core
  workflows) or that causes repeated branching, prefer centralizing the logic and
  modeling state/behavior with types/roles.
repository: cline/cline#v18
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70884
---

When code introduces behavior that’s already implemented elsewhere (utils/formatters/core workflows) or that causes repeated branching, prefer centralizing the logic and modeling state/behavior with types/roles.

Apply these rules:
1) Reuse shared/Core implementations
- If a helper already exists in core/shared, call it instead of re-implementing it in the app.
- If the logic is needed by multiple consumers, move it to the appropriate shared/core module (e.g., next to existing preflight/git utilities) and delete the duplicate runner.

2) Consolidate duplicated formatting/escaping/wrapping
- Keep one formatter that owns escaping and wrapper rules.
- Use a discriminated union to vary only the parts that truly differ (e.g., tool attributes vs run-start source).

Example (single formatter via discriminated union):
```ts
type ToolCtx = { kind: 'tool'; source: string; toolName: string; toolCallId: string; text: string };
type RunStartCtx = { kind: 'runStart'; text: string };
type HookCtx = ToolCtx | RunStartCtx;

function escapeAndNeutralizeHookContext(text: string) {
  return text.trim().replace(/<(\/?)hook_context/gi, '<\\$1hook_context');
}

function formatHookContext(ctx: HookCtx): string {
  const body = escapeAndNeutralizeHookContext(ctx.text);
  if (ctx.kind === 'tool') {
    return `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```

3) Avoid conditional sprawl with a role/strategy
- If you have repeated `if (outputMode === 'json') ... else ...` (or similar), create the correct outputter once at startup (e.g., `JsonRunOutputter` vs `ConsoleRunOutputter`) and then use straight-line calls like `runStarted(...)`, `runResult(...)`, `runAborted(...)`.
- Ensure related concepts (e.g., “verbose” vs “json”) are modeled orthogonally in the outputter behavior.

4) Prefer unions over booleans for multi-state behavior
- For fields like `resumed`, prefer a string union (e.g., `'resume' | 'start' | undefined`) or a discriminated union to prevent invalid combinations and reduce confusing “boolean meaning” across the codebase.

Net effect: fewer duplicated utilities/formatters, clearer control flow, more testable state modeling, and code that’s easier to maintain consistently across app/core boundaries.