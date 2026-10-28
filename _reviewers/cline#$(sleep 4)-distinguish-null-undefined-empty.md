---
title: Distinguish null, undefined, empty
description: Null, undefined, and "empty" (empty string/array) often carry different
  meanings at a boundary (wire protocol, API schema, function parameter), and treating
  them interchangeably causes silent, hard-to-spot bugs. Before writing a null/undefined
  check or using `??`/default values, be explicit about what each state actually means
  for that specific field, and...
repository: cline/cline#$(sleep 4)
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70978
---

Null, undefined, and "empty" (empty string/array) often carry different meanings at a boundary (wire protocol, API schema, function parameter), and treating them interchangeably causes silent, hard-to-spot bugs. Before writing a null/undefined check or using `??`/default values, be explicit about what each state actually means for that specific field, and validate it with real type narrowing rather than loose equality or coalescing.

Concretely:
- When consuming external/untrusted data (RPC responses, protobuf, user input), don't assume the shape matches your type declaration — narrow it. A pagination cursor typed as `string | undefined` can still arrive as `null` from a non-conforming server; `cursor !== undefined` lets it through and loops forever. Use `typeof value === "string" ? value : undefined` instead of relying on strict (or loose) inequality.
- Nullish coalescing (`??`) only falls back on `null`/`undefined`. If the "absent" value is actually an empty array/string (e.g., protobuf decodes an omitted repeated field as `[]`), `??` won't catch it. Check for emptiness explicitly: `images?.length ? images : retry.images`.
- When a parameter has a default value, passing `undefined` is swallowed by that default, while `null` is not. If callers need to distinguish "use default" from "explicitly disable," the signature and the call sites must agree on which sentinel is used — don't let the type annotation drift from the runtime behavior (e.g., widen to `| null` everywhere the value is truly nullable, and keep call sites passing `null` rather than `undefined` when that's the intended sentinel).
- At serialization boundaries, `undefined`/omitted and explicit `null` can mean different things ("leave unchanged" vs "clear"). Make sure encode/decode logic preserves that distinction — e.g., encode a "clear" as `{}`/`null` explicitly rather than collapsing it to an omitted field, and add a regression test for the clear case.

As a rule: for every nullable/optional field, document (in code or a comment) what `null`, `undefined`, and "empty" each signify, and add a test that exercises the case your guard is meant to catch (e.g., a non-advancing or null cursor, an empty-array "no attachments" response, an explicit `null` clear).