---
title: Centralize and Isolate Logic
description: 'Prefer shared, single-source implementations and isolate variation using
  types/roles.


  Apply this when making code clearer and easier to maintain:


  1) Reuse existing helpers/utilities instead of re-implementing'
repository: cline/cline#v19
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70885
---

Prefer shared, single-source implementations and isolate variation using types/roles.

Apply this when making code clearer and easier to maintain:

1) Reuse existing helpers/utilities instead of re-implementing
- If core/shared already normalizes Git remotes, checks refs/upstreams, detects shell kinds, or performs common inference, import and reuse it.
- If the logic belongs in more than one place, move it into the appropriate core module rather than duplicating a second “runner”/utility in an app.

2) Avoid scattered conditionals: use a role/interface created once
- When behavior differs by mode (e.g., json vs console, verbose vs not), create a single “outputter” (or similar role) once at startup and call straight-line lifecycle methods.
- Keep branching inside the factory, not throughout the main run path.

3) Model multi-state flags with unions (not booleans)
- If a boolean doesn’t represent all states (or can become ambiguous), use a string union/discriminated union so invalid states can’t compile and tests are simpler.

4) Consolidate formatting/escaping rules into one place
- If two functions do the same trimming/escaping and only differ by identity/tool metadata, use a discriminated union so the escaping logic lives in one formatter.

Example (state union instead of boolean):
```ts
type ResumeMode =
  | { resumed: false }
  | { resumed: true }
  | { resumed: "client_inherited"; source: "ENV" };

function dispatchStart(ctx: { resumed?: ResumeMode["resumed"] }) {
  // compile-time clear branching on valid states
}
```

Example (single formatter via discriminated union):
```ts
type HookContext =
  | { kind: "tool"; source: string; toolName: string; toolCallId: string; text: string }
  | { kind: "run"; source: "RunStart"; text: string };

function formatHookContext(ctx: HookContext): string {
  const body = ctx.text.trim().replace(/<(\/? )hook_context/gi, "<\\$1hook_context");
  return ctx.kind === "tool"
    ? `<hook_context source="${ctx.source}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`
    : `<hook_context source="${ctx.source}">\n${body}\n</hook_context>`;
}
```

Outcome: fewer duplicated implementations, clearer control flow, fewer invalid states, and one canonical place for formatting/escaping logic.