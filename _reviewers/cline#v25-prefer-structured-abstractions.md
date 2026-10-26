---
title: Prefer structured abstractions
description: When changing code for readability and maintainability, avoid duplicated
  logic and “mode” branching; use expressive types and self-documenting constants.
repository: cline/cline#v25
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70891
---

When changing code for readability and maintainability, avoid duplicated logic and “mode” branching; use expressive types and self-documenting constants.

Apply these rules:
1) Reuse centralized implementations
- If similar logic already exists in core (e.g., git preflight/reader utilities), import and reuse it.
- If the logic should be shared across products, move/own it in the shared core module rather than keeping a second snapshot in an app.

2) Replace repeated `if (mode === ...)` with role-based outputters
- Create outputter implementations (e.g., `JsonRunOutputter`, `ConsoleRunOutputter`) via a factory once, then use straight-line calls (`runStarted`, `runResult`, etc.).
- Ensure orthogonal concerns (e.g., verbose vs output format) flow through outputters consistently.

3) Use string/discriminated unions instead of booleans for state
- Prefer a union that can represent all valid states.
- This prevents “invalid combinations” and makes control-flow clearer and easier to test.

4) Keep formatting/escaping/wrapping rules in one place
- Generalize formatter(s) with a discriminated union (run-start vs tool-hook) so escaping rules are not duplicated.

5) Remove magic numbers
- Extract fixed delays/timeouts into named constants and add a short comment describing intent (e.g., “grace period to drain output”).

Example (single formatter + expressive types + named constant):
```ts
type HookContextOrigin =
  | { kind: "tool"; source: string; toolName: string; toolCallId: string }
  | { kind: "run"; source: "RunStart" };

type EmbeddedEscapingInput = { text: string; origin: HookContextOrigin };

const OUTPUT_DRAIN_GRACE_MS = 1000; // grace period to drain output after process exit

function formatHookContextBlock({ text, origin }: EmbeddedEscapingInput): string {
  const body = text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");

  if (origin.kind === "tool") {
    return `<hook_context source="${origin.source}" tool_name="${origin.toolName}" tool_call_id="${origin.toolCallId}">\n${body}\n</hook_context>`;
  }

  return `<hook_context source="${origin.source}">\n${body}\n</hook_context>`;
}
```

Outcome: code becomes easier to scan (less branching), harder to break (shared logic + single formatter), and easier to evolve (types model valid states, timeouts are documented).