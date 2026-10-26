---
title: Avoid duplicate logic
description: Before adding new logic, search the codebase for an existing implementation
  and reuse or extend it rather than writing a parallel version. This applies to utility
  functions (e.g. shell/PowerShell detection already in `@cline/shared`'s `getShellKind`),
  domain logic (e.g. git snapshot/preflight code already in `core/services/cloud-handoff`),
  and...
repository: cline/cline
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70886
---

Before adding new logic, search the codebase for an existing implementation and reuse or extend it rather than writing a parallel version. This applies to utility functions (e.g. shell/PowerShell detection already in `@cline/shared`'s `getShellKind`), domain logic (e.g. git snapshot/preflight code already in `core/services/cloud-handoff`), and near-duplicate helpers that differ only slightly (e.g. two hook-context formatters that just vary by source type). When two functions share most of their behavior, generalize them into one — for example, use a discriminated union or options object to express the variant-specific parts instead of copy-pasting the shared parts:

```ts
type HookOrigin =
  | { kind: "tool"; toolName: string; toolCallId: string }
  | { kind: "runStart" };

function formatHookContextBlock(text: string, origin: HookOrigin): string {
  const body = text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  const attrs =
    origin.kind === "tool"
      ? ` tool_name="${origin.toolName}" tool_call_id="${origin.toolCallId}"`
      : "";
  return `<hook_context source="${origin.kind}"${attrs}>\n${body}\n</hook_context>`;
}
```

Also respect the dependency direction when deciding where shared logic should live: apps may depend on core/SDK packages, but core/SDK must never depend back on app code, so move logic that both sides need into the lower-level package (e.g. `@cline/core` or `@cline/shared`) rather than duplicating it in the app. Consolidating logic this way keeps behavior consistent, reduces the surface area for bugs, and makes future changes a single-point edit instead of a multi-file hunt.