---
title: Clear Semantic Identifier Naming
description: Adopt naming conventions that are (1) case-consistent by identifier kind
  and (2) semantically self-documenting (what it represents/includes/excludes, and
  what the function returns).
repository: redis/redis
label: Naming Conventions
language: C
comments_count: 10
repository_stars: 74261
---

Adopt naming conventions that are (1) case-consistent by identifier kind and (2) semantically self-documenting (what it represents/includes/excludes, and what the function returns).

**Rules**
1. **Identifier case consistency**
   - Use **camelCase** for **functions** and **global/server variables**.
   - Use **snake_case** for **local variables**.
   - Do not mix styles in the same function/scope.
2. **Names must encode meaning**
   - For metrics/fields/helpers, include/exclude behavior must be evident from the name (or be explicitly documented next to the declaration).
   - Prefer names like `*Shared*` / `*Unshared*` when inclusion varies.
3. **Function names must match behavior**
   - If a function returns a boolean/status (e.g., 0/1), the return meaning must be reflected in the name (e.g., `should...`, `try...`, `is...`) or the code should clearly define it in the comment immediately above the function.
   - Align with existing naming patterns (e.g., `clientsCronRunClient`-style).
4. **Avoid ambiguity for internal concepts**
   - For internal commands or domain terms, avoid unclear abbreviations unless the naming/context makes the value’s meaning obvious; prefer descriptive names or add a precise comment that explains the stored value and its unit.

**Examples**
- Prefer:
  - `mem_clients_ref` / `mem_clients_orphan_ref` (but ensure docs/state match inclusion).
  - `getClientMemoryUsage()` vs `getClientOutputBufferMemoryUsage()` should clearly state inclusion/exclusion; if needed, rename one to reflect it (e.g., “Size” vs “Usage”).
- Prefer boolean-like naming:
  - `int shouldFreeClientAndHandleTimeout(...)` over a generic `cronHandleClients(...)` if the return value drives control flow.
- Enforce case:
  - `uint64_t *kvObjMetaRef(...)` (function: camelCase).
  - `lower_mask` (locals: snake_case).