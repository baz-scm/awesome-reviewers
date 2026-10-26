---
title: Preserve API Contract Semantics
description: 'Treat API-like boundaries (HTTP headers, REST/GraphQL payloads, event
  envelopes, and even cross-layer client calls) as contracts: field *names* and field
  *meaning* must remain consistent end-to-end, and gating/serialization rules should
  follow the spec.'
repository: Cline/Cline
label: API
language: TypeScript
comments_count: 6
repository_stars: 70840
---

Treat API-like boundaries (HTTP headers, REST/GraphQL payloads, event envelopes, and even cross-layer client calls) as contracts: field *names* and field *meaning* must remain consistent end-to-end, and gating/serialization rules should follow the spec.

Apply this:
- **Forward every field** through every projection/copy layer (server → hub → handler, etc.). If a field is accepted at one boundary, it must be emitted at the next.
- **Never silently change semantics behind the same identifier** (e.g., keep the header name aligned with what the value represents, or rename/add a new header).
- **Make spec-driven visibility/gating unconditional**: only expose items that are allowed by the contract; avoid coupling correctness to optional flags.
- **Protect URL/base-path normalization**: rules must not rewrite user-supplied endpoints in ways that change meaning (use provider-specific exceptions explicitly).
- **Use explicit inputs for API-like function signatures**: prefer options objects / discriminated unions over positional booleans so call sites can’t swap meaning.

Example (rename or add header to keep meaning unambiguous):
```ts
// Before (contract ambiguous):
// headers: { "X-Task-ID": ulid }

// After (contract explicit):
headers: {
  "X-Task-ID": taskId,      // if backend expects a task id here
  "X-Task-ULID": ulid,     // if backend also needs ulid
}

// Or (if backend only wants ulid):
// headers: { "X-Task-ULID": ulid }
```

Example (avoid boolean meaning drift):
```ts
// Instead of:
// load(true, true)

// Prefer:
load({ refresh: true, background: true });
```

This prevents “it works but semantics changed” bugs that typically surface as missing/incorrect fields, spec violations, wrong attribution/rate limits, or silent capability downgrade.