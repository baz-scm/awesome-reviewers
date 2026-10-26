---
title: API contract completeness
description: 'Define and enforce API contracts as end-to-end invariants: request/response
  fields, parameter semantics, headers, and versioned endpoints must remain unambiguous
  and must be forwarded consistently across layers.'
repository: cline/cline#v3
label: API
language: TypeScript
comments_count: 5
repository_stars: 70863
---

Define and enforce API contracts as end-to-end invariants: request/response fields, parameter semantics, headers, and versioned endpoints must remain unambiguous and must be forwarded consistently across layers.

Guidelines:
1) Spec-driven behavior first
- Implement spec-required filtering/visibility rules as unconditional invariants; don’t gate “must not list” behavior behind unrelated feature flags.

2) No “accepted-but-not-forwarded” fields
- When an API layer accepts a field (e.g., `displayPrompt`), ensure every downstream projection/event copy and handler forwards it. Add tests that assert equality (including omitted/empty variants) across boundaries.

3) Make wire semantics explicit
- If the meaning of a wire element changes, rename it or send it separately (e.g., keep `X-Task-ID` as task id; introduce `X-Task-ULID`, or add `X-Task-ULID` alongside). Never silently change header payload semantics under the same name.

4) Prefer named option objects over boolean positional parameters
- Replace `load(refresh, background)` / `load(true, true)`-style APIs with `load({ refresh: true, background: true })` to prevent call-site ambiguity.

5) Versioned endpoints + normalization
- Use the correct versioned endpoint paths and normalize base URLs consistently (e.g., strip trailing slashes and optional version prefixes before appending the target version path).

Example (pattern):
```ts
// Prefer explicit options
type LoadArgs = { refresh?: boolean; background?: boolean };
async function load(args: LoadArgs = {}) {
  const { refresh = false, background = false } = args;
  // ...
}

// Preserve field through boundaries
type Input = { prompt: string; displayPrompt?: string };
type Event = { prompt: string; displayPrompt?: string };
function toEvent(input: Input): Event {
  return { prompt: input.prompt, displayPrompt: input.displayPrompt };
}

// Keep header meaning unambiguous
function headers(taskId: string, ulid: string) {
  return {
    "X-Task-ID": taskId,
    "X-Task-ULID": ulid,
  };
}
```