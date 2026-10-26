---
title: Centralize Formatting And Logic
description: When the codebase already has a canonical implementation (git preflight,
  shared command/shell detection, common formatters), don’t re-implement it in another
  layer or create parallel helpers. Instead, centralize shared logic and model variant
  behavior explicitly (roles, factories, discriminated unions) to avoid scattered
  `if/else` branches and duplicated...
repository: cline/cline#v8
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70867
---

When the codebase already has a canonical implementation (git preflight, shared command/shell detection, common formatters), don’t re-implement it in another layer or create parallel helpers. Instead, centralize shared logic and model variant behavior explicitly (roles, factories, discriminated unions) to avoid scattered `if/else` branches and duplicated escaping/wrapping rules.

How to apply:
- Prefer reuse: if a helper exists in core/shared, import and use it instead of adding a near-copy.
- Prefer explicit variation over branching: if you’re threading many conditionals (e.g., JSON vs console output), introduce a small role interface and instantiate once.
- Deduplicate formatters: keep trimming/escaping/wrapper construction in one place; vary only the minimal emitted fields via a discriminated union.
- Keep code in the right module/layer: app snapshots that belong in core should move near the existing core logic.

Example (single formatter via discriminated union):
```ts
type HookContextInput =
  | { kind: "tool"; source: string; toolName: string; toolCallId: string; text: string }
  | { kind: "runStart"; text: string };

function formatHookContext(input: HookContextInput): string {
  const escapeBody = (t: string) =>
    t.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");

  if (input.kind === "tool") {
    const body = escapeBody(input.text);
    return `<hook_context source="${input.source}" tool_name="${input.toolName}" tool_call_id="${input.toolCallId}">\n${body}\n</hook_context>`;
  }

  const body = escapeBody(input.text);
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```