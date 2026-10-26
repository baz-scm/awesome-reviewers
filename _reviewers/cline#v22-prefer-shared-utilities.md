---
title: Prefer shared utilities
description: When implementing new features, avoid duplicating existing logic and
  avoid proliferating conditional branches. Prefer (1) reuse of shared core/util code,
  (2) small strategy/role interfaces chosen once per execution path, (3) discriminated
  union types over booleans for state, and (4) keeping tool-specific code in dedicated
  modules.
repository: cline/cline#v22
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70886
---

When implementing new features, avoid duplicating existing logic and avoid proliferating conditional branches. Prefer (1) reuse of shared core/util code, (2) small strategy/role interfaces chosen once per execution path, (3) discriminated union types over booleans for state, and (4) keeping tool-specific code in dedicated modules.

Apply this as standards:
- Reuse: If similar logic already exists in core/shared (e.g., git preflight/shell detection/formatting), import and extend it rather than re-implementing it locally.
- Consolidate formatting/escaping: Keep text-trimming/tag-escaping/wrapper construction in one place; if variants differ, model them with a discriminated union and let one formatter handle all cases.
- Replace scattered output conditionals: Introduce an outputter/strategy (created once from configuration) so the main run flow is straight-line and lifecycle events stay consistent across output modes.
- Use union types for state: Avoid booleans for multi-state concepts; use string unions (or richer discriminated unions) so invalid combinations can’t be represented.
- Modularize: Move command/tool-specific additions into a tool-level module to prevent unrelated code growth.

Example (state modeling with a string union):
```ts
type ResumeMode = "none" | "resumed";

export type HookRuntimeOptions = {
  resumed?: ResumeMode;
};
```

Example (single formatter via discriminated union):
```ts
type HookContextOrigin =
  | { kind: "tool"; toolName: string; toolCallId: string }
  | { kind: "runStart" };

function formatHookContext(text: string, origin: HookContextOrigin): string {
  const body = text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (origin.kind === "tool") {
    return `<hook_context source="${origin.kind}" tool_name="${origin.toolName}" tool_call_id="${origin.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```