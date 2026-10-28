---
title: Distinguish null from undefined
description: When handling optional or external data, treat `null` and `undefined`
  as distinct, semantically meaningful states rather than interchangeable "empty"
  values, and validate/narrow untrusted input instead of assuming it matches your
  declared type.
repository: cline/cline;
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70964
---

When handling optional or external data, treat `null` and `undefined` as distinct, semantically meaningful states rather than interchangeable "empty" values, and validate/narrow untrusted input instead of assuming it matches your declared type.

Concretely:
- Decide explicitly what each absence value means in your API/schema (e.g. `undefined`/omitted = "no change" or "not specified", while `null` = "explicitly cleared/reset"), and keep that distinction through encoding, decoding, and default-parameter handling. A function signature that says `| undefined` but whose body actually checks for `null` will silently misbehave once a caller passes the real value.
- Never assume external data (servers, models, other processes) will respect your internal type contract. Narrow loosely-typed fields (e.g. JSON from an MCP server, LLM tool-call arguments) to the exact expected type before using them, and fall back to a safe default otherwise. For example, a pagination cursor from an untyped response should be narrowed like:
  ```ts
  cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined;
  ```
  instead of trusting `result.nextCursor` directly, since a server sending `null` would otherwise pass an `!== undefined` check and corrupt the loop.
- When normalizing permissive input (e.g. accepting `null` from models that don't support a field) into a stricter runtime value, do so deliberately and document why, rather than letting `null` silently flow through as if it were `undefined` or an empty string.
- When forwarding values through multiple layers (wire encoding, persistence, RPC), verify that `null` survives as `null` end-to-end if it's meant to signal "clear this field" — an encoding that collapses `null` into `{}` or omits it can turn an explicit clear into a silent no-op.

Add regression tests for these null/undefined edge cases, especially at the boundary where data crosses from an external or loosely-typed source into your typed system.