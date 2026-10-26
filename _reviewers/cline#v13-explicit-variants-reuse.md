---
title: Explicit Variants Reuse
description: 'Prefer shared/core helpers and model variants explicitly to avoid duplicated
  logic and conditional sprawl.


  Apply:

  1) Reuse existing implementations

  - If core/shared already normalizes/checks/reads/formatting, don’t re-create it
  in the app layer. Extract/move the logic into the core package if it’s a true cross-cutting
  concern.'
repository: cline/cline#v13
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70874
---

Prefer shared/core helpers and model variants explicitly to avoid duplicated logic and conditional sprawl.

Apply:
1) Reuse existing implementations
- If core/shared already normalizes/checks/reads/formatting, don’t re-create it in the app layer. Extract/move the logic into the core package if it’s a true cross-cutting concern.

2) Replace boolean state with explicit unions
- When a flag represents a state (or changes semantics), use a string union so invalid combinations can’t occur.

3) Prefer discriminated-union formatters over duplicated formatters
- Keep shared escaping/trimming/wrapper logic in one place; only vary the minimal fields.

4) Isolate output differences behind a role/factory
- Pick the appropriate outputter once (e.g., JSON vs console) and then use straight-line lifecycle calls; let outputters decide what to ignore.

5) In async/cleanup code, remove magic numbers
- Use named constants and document the purpose (e.g., a grace period for draining output after process exit).

Example (variant modeling + single formatter + role boundary):

```ts
type SessionResume = "new" | "resumed";

type HookContext =
  | { kind: "tool"; toolName: string; toolCallId: string; body: string }
  | { kind: "runStart"; body: string };

function formatHookContext(ctx: HookContext): string {
  const body = ctx.body
    .trim()
    .replace(/<(\/?)(hook_context)/gi, "<$1$2");

  return ctx.kind === "tool"
    ? `<hook_context source="Tool" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`
    : `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```

This combination reduces duplication, makes state transitions/test cases clearer, and keeps complex lifecycle code easier to maintain.