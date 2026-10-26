---
title: Centralize Variants and Roles
description: 'When implementing new behavior, avoid parallel/duplicated logic and
  make branching explicit via types and roles.


  Apply these rules:

  1) Reuse or centralize shared logic'
repository: cline/cline#v17
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70883
---

When implementing new behavior, avoid parallel/duplicated logic and make branching explicit via types and roles.

Apply these rules:
1) Reuse or centralize shared logic
- If core/shared already performs the normalization/preflight/command-detection/formatting you’re re-implementing, import it instead of copying.
- If the logic is truly app-specific, consider moving it into the appropriate core/shared module to prevent a second implementation living in another layer.

2) Replace scattered conditionals with one role created once
- Don’t thread `if (outputMode === "json")` (or similar) through many call sites.
- Create the appropriate outputter/strategy once at the start (factory), then use straight-line lifecycle calls.

3) Model state with discriminated/string unions, not booleans
- Booleans tend to express ambiguous/invalid combinations and proliferate.
- Use string unions (or discriminated unions) so invalid states are unrepresentable and handlers are clearer.

4) Consolidate formatting/escaping in one place
- If you need different wrappers/attributes for variants (tool vs run-start), keep one formatter function that switches on a discriminant, while preserving identical trimming/escaping rules.

Sketch:
```ts
type RunContext =
  | { kind: "tool"; source: string; toolName: string; toolCallId: string; text: string }
  | { kind: "run_start"; text: string };

function formatHookContext(ctx: RunContext): string {
  const body = ctx.text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (ctx.kind === "tool") {
    return `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```

Impact: code becomes easier to read, easier to test (types encode valid states), and less error-prone by preventing divergence between duplicated implementations.