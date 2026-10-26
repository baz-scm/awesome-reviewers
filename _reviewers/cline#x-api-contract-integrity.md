---
title: API contract integrity
description: Ensure every externally observable interface (request headers, URLs,
  payload fields, and spec-driven filtering) is contract-correct, self-describing,
  and fully propagated—without “conditional” behavior that breaks the spec.
repository: cline/cline#x
label: API
language: TypeScript
comments_count: 6
repository_stars: 70861
---

Ensure every externally observable interface (request headers, URLs, payload fields, and spec-driven filtering) is contract-correct, self-describing, and fully propagated—without “conditional” behavior that breaks the spec.

Apply these rules:
- **Spec-driven logic should be unconditional.** If the host MUST NOT list tools that lack `visibility` containing `"model"`, do not re-enable listing via options; keep behavior spec-true.
- **Propagate schema changes end-to-end.** When you add a field like `displayPrompt`, forward it through *all* event projections/copies (and ensure omitted/empty cases are handled consistently).
- **Preserve header semantics.** If `X-Task-ID` is an attribution/rate-limit identifier, don’t silently change its meaning (e.g., taskId → ulid). Either keep the original semantics, rename the header (e.g., `X-Task-ULID`), or send both as separate headers.
- **Use self-describing parameters.** Avoid boolean positional params that are easy to mix up; prefer an options object.
- **Don’t mutate bootstrap/input truth.** If an observer/host layer adds data for its own bookkeeping, don’t rewrite core-visible fields in the API input (e.g., don’t accidentally mark a session as a resume by injecting `config.sessionId`).
- **Versioned URLs must be normalized.** Ensure you’re using the correct API version path (`/api/v1/...` vs `/api/v0/...`) and normalize trailing slashes/prefixes consistently.

Example (options object instead of booleans):
```ts
// Instead of load(true, true)
load({ refresh: true, background: true });
// Optionally:
function load(args: { refresh?: boolean; background?: boolean }) {
  const { refresh = false, background = false } = args;
  // ...
}
```

Example (header semantics):
```ts
// Prefer either:
"X-Task-ID": taskId,
"X-Task-ULID": ulid,
// or rename the header if semantics change.
```