---
title: Avoid duplicated logic
description: 'When implementing code paths with variants (output modes, hook/run context,
  resumed state, shell detection), avoid duplicating existing helpers/logic and avoid
  boolean/conditional sprawl. Instead:'
repository: cline/cline#v3
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70863
---

When implementing code paths with variants (output modes, hook/run context, resumed state, shell detection), avoid duplicating existing helpers/logic and avoid boolean/conditional sprawl. Instead:

- Reuse the existing implementation from the appropriate layer (e.g., core/shared utilities) rather than adding a parallel helper in the app.
  - If the needed behavior belongs in core, move/extend it there next to the related functionality (don’t keep a second git runner or duplicate shell detection).

- Isolate variant handling behind a single abstraction boundary:
  - Use a factory + role/interface (e.g., `JsonRunOutputter`/`ConsoleRunOutputter`) so the rest of the function is straight-line lifecycle calls.
  - Or use a discriminated union for “kinds” (run-start vs tool-hook; resumed vs not) so escaping/formatting rules live in one place.

- Prefer explicit state modeling over booleans for variant states:
  - Use a string union (or discriminated union) so only valid combinations are representable and tests are easier.

- Keep modules cohesive:
  - Don’t add large blocks of tool-specific code into generic/shared modules; split into tool-level modules.

Example (discriminated-union formatter to avoid two near-identical formatters):
```ts
type HookContext =
  | { kind: "tool"; source: string; toolName: string; toolCallId: string; body: string }
  | { kind: "runStart"; body: string };

function escapeEmbeddedHookTags(text: string) {
  return text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
}

function formatHookContext(ctx: HookContext): string {
  const body = escapeEmbeddedHookTags(ctx.body);
  if (ctx.kind === "tool") {
    return `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```

Use this checklist during review:
1) “Is any logic duplicated elsewhere (core/shared/util)?”
2) “Are we threading `if (mode === ...)` conditionals through many call sites?”
3) “Are variant states modeled as booleans instead of unions?”
4) “Is code located in a module that matches its domain responsibility?”