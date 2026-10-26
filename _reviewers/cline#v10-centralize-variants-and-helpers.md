---
title: Centralize Variants and Helpers
description: When implementing logic that has multiple modes/variants (formatting,
  output, execution context, platform checks), avoid duplicating existing helpers
  and avoid scattering conditionals across the codebase.
repository: cline/cline#v10
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70869
---

When implementing logic that has multiple modes/variants (formatting, output, execution context, platform checks), avoid duplicating existing helpers and avoid scattering conditionals across the codebase.

Apply these rules:
- Reuse shared implementations: Before adding a new “runner/normalizer/check,” search for an existing function in `core/` or `sdk/shared` and call it. If the behavior belongs to the platform/framework layer, move the logic there (instead of maintaining an app-local copy).
- Use role/strategy objects for mode switching: If code branches on `outputMode` (or similar) in many places, create an outputter/formatter object once (e.g., via a small factory) and then call straight-line lifecycle methods.
- Prefer discriminated unions over booleans for state: If a flag can represent more than two meaningful states (or leads to invalid combinations), use a string union and model each variant explicitly.
- Centralize shared formatting/escaping rules: If two formatters trim/escape/wrap the same way, unify them into one formatter that branches on a variant type, so escaping rules live in one place.

Example (pattern):
```ts
type HookContextVariant =
  | { kind: "tool"; toolName: string; toolCallId: string; source: string }
  | { kind: "runStart"; source: string };

function formatHookContextBlock(text: string, v: HookContextVariant): string {
  const body = text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (v.kind === "tool") {
    return `<hook_context source="${v.source}" tool_name="${v.toolName}" tool_call_id="${v.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="${v.source}">\n${body}\n</hook_context>`;
}
```
