---
title: Stable, explicit API contracts
description: Treat every API/SDK boundary (request headers, endpoint paths, list/filter
  semantics, and multi-flag inputs) as a *contract* that must remain self-describing
  and spec-compliant.
repository: cline/cline#v11
label: API
language: TypeScript
comments_count: 5
repository_stars: 70871
---

Treat every API/SDK boundary (request headers, endpoint paths, list/filter semantics, and multi-flag inputs) as a *contract* that must remain self-describing and spec-compliant.

Apply these rules:
1) Follow spec/protocol gating unconditionally
- Don’t add “host capability present” exceptions when the spec defines the correct behavior.
- Example pattern:
  ```ts
  // Correct: always enforce "model" visibility
  const visible = descriptors.filter(d => d.visibility?.includes("model"));
  return visible;
  ```

2) Prefer typed options objects over boolean positional parameters
- Boolean flags are easy to mix up and hard to read.
- Example:
  ```ts
  // Prefer
  load({ refresh: true, userInitiated: true });

  // Over
  load(true, true);
  ```

3) Preserve semantic meaning of request fields
- If you change what a field represents, rename the field or add a separate one.
- Never silently swap payload meaning while keeping the same header/parameter name (e.g., `X-Task-ID` must always carry the task id; if it carries ULID now, rename to `X-Task-ULID` or send both).

4) Make endpoint versioning + URL normalization explicit and consistent
- Ensure code and comments describe the *current* runtime rule.
- Handle trailing slashes and optional version prefixes deterministically, and add coverage for common variants.

Net effect: fewer silent behavior changes, fewer ambiguity-driven bugs, and safer evolution of API-compatible request/response formats.