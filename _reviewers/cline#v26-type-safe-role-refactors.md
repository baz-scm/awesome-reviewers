---
title: Type-Safe Role Refactors
description: When refactoring for readability, prefer type-driven design and strategy/role
  objects over duplicated logic, scattered conditionals, and ambiguous boolean flags.
repository: cline/cline#v26
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70893
---

When refactoring for readability, prefer type-driven design and strategy/role objects over duplicated logic, scattered conditionals, and ambiguous boolean flags.

Apply these rules:
1) Replace boolean/flag state with unions
- If a flag represents multiple meaningful states (or can’t capture invalid combinations), use a string union (or discriminated union) rather than boolean.

2) Avoid threading conditionals through the code
- Create the appropriate strategy/role object once (e.g., an outputter/formatter) and dispatch straight-line lifecycle calls (started/result/aborted). This keeps “what to do” separate from “when to do it.”

3) Generalize duplicated formatting/escaping into one typed formatter
- If two formatters differ only by “tool vs run-start” identity, unify them using a discriminated union so escaping/neutralization rules live in one place.

4) Reuse core/shared logic or extract tool-scoped modules
- Don’t re-implement core behavior in app snapshots when existing utilities already normalize/validate data. If the code is truly tool-specific, move it into a tool-level module rather than bloating shared areas.

5) Keep imports tight
- Remove unused or now-unneeded imports after refactors; reuse existing helpers from shared packages.

Example pattern (unified formatter via discriminated union):
```ts
type HookContext =
  | { kind: "tool"; source: string; toolName: string; toolCallId: string; body: string }
  | { kind: "run"; source: "RunStart"; body: string };

function formatHookContext(ctx: HookContext): string {
  const body = ctx.body
    .trim()
    .replace(/<(\/?)hook_context/gi, "<\\$1hook_context");

  return ctx.kind === "tool"
    ? `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`
    : `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```

Outcome: code becomes easier to read, test, and extend because state is explicit in types, duplicated logic is consolidated, and runtime behavior is selected via clear roles rather than scattered conditionals.