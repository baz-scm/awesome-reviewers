---
title: Explicit API Contracts
description: All API interfaces (public functions, HTTP headers, event/envelope payloads,
  and versioned endpoints) must be contract-correct, unambiguous, and round-tripped
  end-to-end.
repository: cline/cline#v19
label: API
language: TypeScript
comments_count: 5
repository_stars: 70885
---

All API interfaces (public functions, HTTP headers, event/envelope payloads, and versioned endpoints) must be contract-correct, unambiguous, and round-tripped end-to-end.

Apply this standard:
- **Follow the spec without exception**: if a rule is contractually required (e.g., tool visibility), implement it unconditionally.
- **Preserve field semantics end-to-end**: if a field is accepted/produced, ensure every intermediate projector/handler forwards it back out. Add a payload round-trip test (field present, empty, omitted).
- **Make parameters self-describing**: avoid boolean flag parameters in API surfaces; use an options object with named properties.
- **Never silently change meaning of an identifier**: if `X-Task-ID` starts carrying a different value, either keep the original meaning or rename/version the header (e.g., `X-Task-ULID`) or split into separate headers.
- **Handle API versioning and URL normalization consistently**: implement normalization (trailing slashes, optional `/v1`, base-path prefixes) before appending versioned paths.
- **Update all consumers when response shapes change**: structured/typed payload changes require renderer/extractor updates, not just the producer.

Example (replace ambiguous booleans with options):
```ts
// Before: unclear call-site semantics
load(true, true);

// After: explicit API
load({ refresh: true, background: true });
```

Example (header contract stability):
```ts
// Either keep semantics stable
"X-Task-ID": taskId ?? ""

// Or make the contract unambiguous
"X-Task-ULID": ulid ?? ""
// (optionally: keep X-Task-ID for taskId if both are needed)
```