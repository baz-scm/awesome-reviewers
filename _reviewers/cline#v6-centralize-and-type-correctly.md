---
title: Centralize and type correctly
description: 'Prefer designs that keep shared behavior in one place and make valid
  states explicit.


  Apply these rules:

  - Reuse existing core utilities instead of duplicating logic in apps. If the needed
  functionality is missing, move the snapshot/runner logic into the appropriate shared
  core module rather than introducing a parallel implementation.'
repository: cline/cline#v6
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70864
---

Prefer designs that keep shared behavior in one place and make valid states explicit.

Apply these rules:
- Reuse existing core utilities instead of duplicating logic in apps. If the needed functionality is missing, move the snapshot/runner logic into the appropriate shared core module rather than introducing a parallel implementation.
- Remove scattered output branching. Pick a single output “strategy” once (via a small factory) and then call straight-line lifecycle methods; ensure orthogonal concerns (e.g., verbosity vs output format) flow through the same abstraction.
- Model multi-state concepts with string/discriminated unions, not booleans, to prevent invalid state combinations and improve testability.
- Consolidate duplicated formatting/escaping logic behind one generalized formatter driven by a discriminated union.
- Keep modules cohesive: split tool-specific additions into tool-level modules, and remove now-unused imports/logic after refactors.

Example (unified formatter + discriminated union idea):
```ts
type HookContext =
  | { kind: "tool"; toolName: string; toolCallId: string; text: string }
  | { kind: "runStart"; text: string };

function formatHookContext(ctx: HookContext): string {
  const body = ctx.text
    .trim()
    .replace(/<(\/?)hook_context/gi, "<\\$1hook_context");

  if (ctx.kind === "tool") {
    return `<hook_context source="${ctx.toolName}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">${body}</hook_context>`;
  }
  return `<hook_context source="RunStart">${body}</hook_context>`;
}
```