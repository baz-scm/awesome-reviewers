---
title: Prefer reuse and unions
description: When code must vary by state, output mode, or variant, model it with
  expressive types (discriminated unions / roles) and centralize shared logic. Avoid
  duplicating helpers/formatters or threading conditionals throughout the call stack.
repository: cline/cline#v20
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70886
---

When code must vary by state, output mode, or variant, model it with expressive types (discriminated unions / roles) and centralize shared logic. Avoid duplicating helpers/formatters or threading conditionals throughout the call stack.

Guidelines:
- Replace boolean flags with a string (or enum) union when multiple meaningful states exist.
- Prefer a role/factory pattern (e.g., `RunOutputter`) to isolate `outputMode` branching at construction time, not on every event.
- Use a single formatter for closely related variants; drive differences with a discriminated union rather than copying trim/escaping/wrapper logic.
- Reuse shared utilities from core/shared packages; delete redundant local helpers and remove unused imports when you switch.
- If a change is substantially tool/module-specific, split it into a dedicated tool-level module to keep responsibilities cohesive.

Example (role + union-driven formatting):
```ts
type RunOrigin =
  | { kind: "tool"; toolName: string; toolCallId: string }
  | { kind: "run" };

function formatHookContext(text: string, origin: RunOrigin): string {
  const body = text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (origin.kind === "tool") {
    return `<hook_context source="${"Tool"}" tool_name="${origin.toolName}" tool_call_id="${origin.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}

interface RunOutputter {
  runStarted(): void;
  runResult(result: unknown): void;
  runAborted(err: unknown): void;
}
```

Apply this during review by checking: (1) are we duplicating logic that exists elsewhere, (2) are we scattering `if (mode === ...)` checks, (3) are we using booleans where a union would clarify states, and (4) are closely related formatting rules centralized and covered by tests.