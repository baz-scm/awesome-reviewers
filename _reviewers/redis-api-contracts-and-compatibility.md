---
title: API Contracts And Compatibility
description: 'When adding or evolving APIs (commands, module interfaces, persistence
  callbacks), make the contract explicit and stable: define lifecycle rules, invariants,
  grammar, and compatibility boundaries, and ensure implementations preserve existing
  behavior (including error/return types) across encodings and versions.'
repository: redis/redis
label: API
language: C
comments_count: 8
repository_stars: 74261
---

When adding or evolving APIs (commands, module interfaces, persistence callbacks), make the contract explicit and stable: define lifecycle rules, invariants, grammar, and compatibility boundaries, and ensure implementations preserve existing behavior (including error/return types) across encodings and versions.

Practical rules:
- Define deterministic lifecycle constraints: e.g., “only allowed during OnLoad” for registration-type APIs; document what happens if called elsewhere.
- Establish strong invariants for callbacks: document when callbacks run/are skipped (e.g., “only invoked when meta != reset_value”) so modules can rely on it.
- Version persistence with clear dispatch: use an encoding version (metaver) and specify how load/save behaves for older/newer versions; require modules to handle incompatibility explicitly.
- Keep user-visible semantics encoding-independent: if the API offers BYINT vs BYFLOAT, ensure validation and error/reply behavior matches the selected mode, not the underlying representation.
- Preserve argument grammar and error behavior: if you introduce a parsing abstraction (table/descriptor), ensure it doesn’t change permissible argument order/placement, validation depth, or failure reply semantics.
- Avoid leaking internal implementation details into user responses: internal encodings/representation should not change user-visible replies unless the API explicitly documents it.

Example invariant pattern (persistence/module callbacks):
```c
// Contract: core guarantees callback invocation only when meta != reset_value.
// Modules can safely free/cleanup only under that condition.
if (meta != reset_value) {
    myMeta_free_callback(keyname, meta);
}
```

Apply the same discipline to command grammar (e.g., optional params like IDS/FORCE) and to event subscription APIs: define whether duplicates are allowed, whether deregistration is strict or best-effort, and what constitutes misuse vs supported behavior.