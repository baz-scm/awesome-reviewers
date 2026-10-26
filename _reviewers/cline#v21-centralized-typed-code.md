---
title: Centralized Typed Code
description: 'Prefer code patterns that keep shared behavior single-sourced, reduce
  conditional sprawl, and model state explicitly.


  Apply these rules:

  - **Reuse core utilities**: if equivalent logic already exists in core/shared modules,
  call it instead of duplicating (or move the new logic into core where it belongs).'
repository: cline/cline#v21
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 70886
---

Prefer code patterns that keep shared behavior single-sourced, reduce conditional sprawl, and model state explicitly.

Apply these rules:
- **Reuse core utilities**: if equivalent logic already exists in core/shared modules, call it instead of duplicating (or move the new logic into core where it belongs).
- **Single-source complex formatting/escaping**: when two functions differ only by metadata (e.g., tool vs run-start), unify them behind one formatter with a discriminated input type so escaping/trimming rules live in one place.
- **Use role/factory to avoid scattered `if (outputMode...)`**: create the correct output handler once at startup (e.g., `JsonRunOutputter` vs `ConsoleRunOutputter`) and then call consistent lifecycle methods.
- **Prefer union/string types over booleans for state**: booleans proliferate and allow invalid combinations; use a union such as `'start' | 'resume'`.
- **Keep imports/APIs tidy**: don’t import unused modules; avoid redundant wrappers/accessors unless they add clear value.

Example (pattern):
```ts
type ResumeState = { kind: 'start' } | { kind: 'resume' };

function dispatchRunState(state: ResumeState) {
  return state.kind === 'resume' ? 'agent_resume' : 'agent_start';
}

type HookCtx =
  | { kind: 'tool'; toolName: string; toolCallId: string; text: string }
  | { kind: 'run-start'; text: string };

function formatHookContext(ctx: HookCtx): string {
  const body = ctx.text.trim().replace(/<(\/?)hook_context/gi, '<\\$1hook_context');
  return ctx.kind === 'tool'
    ? `<hook_context source="${ctx.toolName}" tool_name="${ctx.toolName}" tool_call_id="${ctx.toolCallId}">\n${body}\n</hook_context>`
    : `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```