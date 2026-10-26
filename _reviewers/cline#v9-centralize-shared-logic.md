---
title: Centralize Shared Logic
description: 'Prefer centralized, reusable, and well-typed abstractions over duplicated
  logic and ad-hoc conditionals.


  **Apply these rules:**

  1. **Reuse shared core/SDK helpers** instead of reimplementing “the same thing”
  in apps or feature modules (e.g., remote/branch checks, shell kind detection, path
  normalization).'
repository: cline/cline#v9
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70868
---

Prefer centralized, reusable, and well-typed abstractions over duplicated logic and ad-hoc conditionals.

**Apply these rules:**
1. **Reuse shared core/SDK helpers** instead of reimplementing “the same thing” in apps or feature modules (e.g., remote/branch checks, shell kind detection, path normalization).
2. **Avoid conditional sprawl:** if behavior diverges by mode (e.g., JSON vs console, verbose vs non-verbose), create a single strategy/role once (via a factory) and make the execution path “straight-line” with method calls.
3. **Centralize formatting/escaping rules:** don’t add parallel formatters that repeat trim/escape/wrapper logic; use a **discriminated union** so one formatter owns the shared escaping and emits variant-specific attributes.
4. **Use expressive types for state:** prefer **string unions** (or tagged unions) over booleans when multiple states exist or are likely to expand.
5. **Keep modules focused:** move command/tool-specific (or other domain-specific) logic into dedicated modules to prevent large, mixed-purpose files.

**Sketch (strategy + discriminated union):**
```ts
type RunEvent =
  | { kind: "tool"; tool_name: string; tool_call_id: string; body: string }
  | { kind: "runStart"; body: string };

function formatHookContext(e: RunEvent): string {
  const body = e.body.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  if (e.kind === "tool") {
    return `<hook_context source="Tool" tool_name="${e.tool_name}" tool_call_id="${e.tool_call_id}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}

function makeOutputter(outputMode: "json" | "console", verbose: boolean) {
  return outputMode === "json"
    ? new JsonRunOutputter({ verbose })
    : new ConsoleRunOutputter({ verbose });
}
```

Result: fewer duplicated implementations, clearer lifecycle/formatting rules, more testable branching, and consistent behavior across the codebase.