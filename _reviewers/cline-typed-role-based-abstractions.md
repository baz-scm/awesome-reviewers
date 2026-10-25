---
title: Typed Role-Based Abstractions
description: 'When behavior varies (output format, hook origin, execution state),
  avoid scattering conditionals and duplicated helpers/formatters. Instead:


  - Centralize branching behind a small set of role objects created once (e.g., a
  RunOutputter factory) so the main flow stays straight-line.'
repository: CLINE/CLINE
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70837
---

When behavior varies (output format, hook origin, execution state), avoid scattering conditionals and duplicated helpers/formatters. Instead:

- Centralize branching behind a small set of role objects created once (e.g., a RunOutputter factory) so the main flow stays straight-line.
- Model state with expressive types:
  - Prefer string unions (or discriminated unions) over booleans for anything with multiple meaningful states.
  - Use discriminated unions to keep escaping/trimming/wrapping logic in one formatter instead of maintaining parallel formatter functions.
- Reuse shared utilities/modules for common checks/logic instead of adding local equivalents.
- Keep files focused: if code is tool-/command-specific, move it into a dedicated module.

Example (formatter with a discriminated union and one escaping path):

```ts
type ToolHookCtx = {
  kind: "tool";
  source: string;
  toolName: string;
  toolCallId: string;
  body: string;
};

type RunHookCtx = {
  kind: "runStart";
  body: string;
};

type HookCtx = ToolHookCtx | RunHookCtx;

function formatHookContext(ctx: HookCtx): string {
  const body = ctx.body
    .trim()
    .replace(/<(\/? )hook_context/gi, "<\\$1hook_context");

  if (ctx.kind === "tool") {
    return `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`;
  }

  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```

Apply this to keep code easier to read, test, and extend: the “what varies” becomes explicit in types/roles, while the “how it’s formatted/processed” stays centralized.