---
title: Centralize Shared Logic
description: Prefer centralized, reusable implementations for common behavior, and
  model variability with clear interfaces/discriminated unions instead of scattered
  conditionals or booleans.
repository: cline/cline#v5
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70864
---

Prefer centralized, reusable implementations for common behavior, and model variability with clear interfaces/discriminated unions instead of scattered conditionals or booleans.

Guidelines:
- Reuse existing shared utilities/modules (core/shared packages) for logic such as git preflight, shell detection, path normalization, and formatting/escaping.
  - If the logic conceptually belongs to a core concern (e.g., git handling), move it next to the existing core implementation rather than adding a second app-specific runner.
- Avoid duplicating “rule sets” (trimming, tag escaping, wrapper construction). Keep those rules in one formatter/helper and parameterize via a discriminated union.
- Replace booleans with discriminated unions (string/enum unions) when the boolean introduces more than two meaningful states or allows invalid combinations.
- Encapsulate output/behavior differences behind an interface/strategy created once at the boundary (e.g., JSON vs console outputters), so the execution path stays straight-line.

Example (discriminated union over boolean + single formatter):
```ts
type HookContext =
  | { kind: "tool"; toolName: string; toolCallId: string; source: string; body: string }
  | { kind: "runStart"; source: string; body: string };

function escapeAndWrap(body: string): string {
  return body
    .trim()
    .replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
}

function formatHookContext(ctx: HookContext): string {
  const escapedBody = escapeAndWrap(ctx.body);
  if (ctx.kind === "tool") {
    return `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${escapedBody}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${escapedBody}\n</hook_context>`;
}
```

If you need a new behavior variant (output mode, hook subtype, run state), add it to the union/interface and update the single centralized implementation—don’t fork duplicated logic across app/runtime layers.