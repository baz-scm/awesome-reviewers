---
title: Prefer shared abstractions
description: Before adding new logic, check whether the same behavior already exists
  in core/shared modules. If so, reuse it instead of duplicating (including small
  helpers).
repository: Cline/Cline
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70840
---

Before adding new logic, check whether the same behavior already exists in core/shared modules. If so, reuse it instead of duplicating (including small helpers).

When behavior varies (e.g., output modes), avoid threading conditionals throughout the call chain; create a strategy/role once (via a factory) and then use straight-line lifecycle calls.

If you’re adding near-duplicate formatting/escaping/wrapping, consolidate into a single formatter with a discriminated union so the escaping rules live in one place.

Also, keep code organization clean: if a change introduces tool-specific complexity, split it into a dedicated tool-level module rather than growing general-purpose files.

Example (strategy pattern for mode):
```ts
const outputter = createRunOutputter({
  outputMode: config.outputMode,
  verbose: config.verbose,
});

outputter.runStarted(...);
// straight-line calls; outputter decides what to emit
outputter.runResult(...);
outputter.runAborted(...);
```

Example (single formatter with origin):
```ts
type HookOrigin =
  | { kind: "tool"; toolName: string; toolCallId: string }
  | { kind: "runStart" };

function formatHookContext(text: string, origin: HookOrigin) {
  const body = text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (origin.kind === "tool") {
    return `<hook_context source="${source}" tool_name="${origin.toolName}" tool_call_id="${origin.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```