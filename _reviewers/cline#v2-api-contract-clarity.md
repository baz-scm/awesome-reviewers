---
title: API contract clarity
description: Ensure every outward-facing interface (REST endpoints, headers, event
  payloads, tool listings) is *semantically consistent with its contract* and *unambiguous
  at the call site*.
repository: cline/cline#v2
label: API
language: TypeScript
comments_count: 5
repository_stars: 70861
---

Ensure every outward-facing interface (REST endpoints, headers, event payloads, tool listings) is *semantically consistent with its contract* and *unambiguous at the call site*.

Practical rules:
- **Conform to the spec without hidden exceptions.** If the contract says “MUST NOT list tools whose visibility doesn’t include \"model\",**do it unconditionally**—don’t condition behavior on unrelated capability flags.
- **Propagate new/required fields end-to-end.** If an upstream API accepts a field (e.g., `displayPrompt`), ensure it is forwarded through all adapters/projections so it can’t disappear silently.
- **Keep identifier semantics aligned with their names.** If you change what a header value represents, **rename the header** (e.g., `X-Task-ULID`) or add a second header; don’t reuse `X-Task-ID` for a different meaning.
- **Use explicit, typed option objects instead of boolean parameters** in exported APIs, so meaning is readable without scrolling.
- **Update endpoint paths/versions deliberately and consistently.** When upstream versions change, align your request URL and normalize prefixes/trailing slashes so the effective path is correct.

Example (replace boolean params with named options):
```ts
// Bad: caller can’t tell what each boolean means
load(true, false)

// Good: explicit API intent
load({ refresh: true, userInitiated: false })
```