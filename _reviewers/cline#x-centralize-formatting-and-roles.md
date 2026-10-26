---
title: Centralize formatting and roles
description: When code needs to support multiple modes/states, prioritize readability
  by centralizing shared logic and replacing conditional sprawl with clear abstractions.
repository: cline/cline#x
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70861
---

When code needs to support multiple modes/states, prioritize readability by centralizing shared logic and replacing conditional sprawl with clear abstractions.

Apply these rules:
- Reuse existing core/shared utilities instead of re-implementing the same behavior in an app layer.
- Consolidate duplicated formatting/escaping/wrapping logic into a single formatter/utility. If there are variant shapes (e.g., tool-hook vs run-start), model them with a discriminated union and have one formatter decide the wrapper fields.
- Avoid scattering `if (outputMode === "json") ... else ...` throughout the execution path. Create the appropriate outputter (e.g., `JsonRunOutputter` / `ConsoleRunOutputter`) once via a factory, and use straight-line calls (`runStarted`, `runResult`, `runAborted`, …).
- Use string unions for multi-state options instead of booleans (so invalid combinations can’t silently appear).
- When refactoring wrappers around callbacks, preserve intended `this`/receiver semantics explicitly (don’t accidentally change what `this` refers to).

Example (single formatter via discriminated union):
```ts
type HookOrigin =
  | { kind: "tool"; toolName: string; toolCallId: string; source: string }
  | { kind: "runStart"; source: string };

function formatHookContextBlock(text: string, origin: HookOrigin): string {
  const body = text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (origin.kind === "tool") {
    return `<hook_context source="${origin.source}" tool_name="${origin.toolName}" tool_call_id="${origin.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="${origin.source}">\n${body}\n</hook_context>`;
}
```