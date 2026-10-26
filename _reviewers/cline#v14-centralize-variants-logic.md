---
title: Centralize Variants Logic
description: When code behavior differs by context (output mode, run-start vs tool-hook,
  OS/shell type, etc.), avoid duplicating logic and avoid scattering conditionals.
repository: cline/cline#v14
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70876
---

When code behavior differs by context (output mode, run-start vs tool-hook, OS/shell type, etc.), avoid duplicating logic and avoid scattering conditionals.

Apply these rules:
- Reuse existing shared utilities/core logic. Don’t reimplement the same git checks, shell detection, or path normalization in higher layers—import from the shared/core package or move the shared behavior into core next to the existing implementation.
- Centralize variant-specific behavior using a small abstraction (strategy/role/factory) or a discriminated union. This keeps branching at one creation site instead of threading `if` statements throughout the call chain.
- Prefer explicit union types over booleans when more than two states or “invalid combinations” exist (e.g., model resume state with a union rather than `true/false`).
- Centralize complex formatting/escaping in one place: generalize existing formatters instead of adding a second near-duplicate.
- Split large, domain/tool-specific additions into dedicated modules to prevent app-level bloat.

Example (union vs boolean + single formatter):
```ts
type ResumeState =
  | { resumed: false }
  | { resumed: true; agentResumeType: "client" | "hub" };

type HookContext =
  | { kind: "tool"; toolName: string; toolCallId: string; body: string }
  | { kind: "runStart"; body: string };

function formatHookContext(ctx: HookContext): string {
  const escaped = ctx.body.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (ctx.kind === "tool") {
    return `<hook_context source="Tool" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${escaped}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${escaped}\n</hook_context>`;
}
```

Net effect: less duplicated logic, fewer fragile branches, clearer invariants, and easier maintenance.