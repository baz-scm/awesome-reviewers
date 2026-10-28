---
title: Distinguish null, undefined, empty
description: 'Several bugs came from treating `null`, `undefined`, and "empty" values
  (`[]`, `{}`) as interchangeable, especially at serialization/transport boundaries
  (JSON-RPC, protobuf, daemon APIs) where each has a distinct, deliberate meaning.
  Loose checks like `value !== undefined` or `value ?? fallback` silently let the
  wrong sentinel through:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70965
---

Several bugs came from treating `null`, `undefined`, and "empty" values (`[]`, `{}`) as interchangeable, especially at serialization/transport boundaries (JSON-RPC, protobuf, daemon APIs) where each has a distinct, deliberate meaning. Loose checks like `value !== undefined` or `value ?? fallback` silently let the wrong sentinel through:

- An MCP server returning `"nextCursor": null` passed `!== undefined` and kept paginating forever, because the code never narrowed the value to the only type it should accept (`string`).
- Protobuf decodes an omitted `images` field as `[]`, not `undefined`, so `images ?? retry.images` always kept the empty array instead of falling back — the check needed to test for actual emptiness (`images?.length ? images : retry.images`), not nullishness.
- Encoding a metadata "clear" as literal `null` was decoded by `asPlainRecord` as "omitted," turning an intended wipe into a silent no-op; the deliberate `{}` encoding had to be restored to preserve that semantic.
- Accepting `null` for a field that should only ever be a string requires an explicit, documented normalization step (e.g., "treat null as omitted at the call site") rather than widening the type and hoping downstream code handles it.

When writing code that consumes external or serialized data (RPC results, protobuf messages, persisted records, third-party APIs):
1. Narrow values to the exact type you expect before branching on them; don't assume `!== undefined` or `??` catches every "absent" representation the source can produce.
2. Identify all the ways "nothing" can be represented (`null`, `undefined`, `[]`, `{}`, omitted key) and handle each explicitly and intentionally — document which ones are treated as equivalent and why.
3. When a null/undefined branch represents an error or invariant violation (e.g., required artifacts are still missing after an operation that should have set them), fail loudly (throw) instead of silently falling through to a path that assumes the value is present.

```ts
// Bad: assumes server always sends a string or omits the field entirely
cursor = result.nextCursor;

// Good: narrow explicitly, treat any non-string as "no more pages"
cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined;

// Bad: "??" only guards against null/undefined, not an empty array sentinel
await initTask(retry.prompt, images ?? retry.images, files);

// Good: check the actual condition you care about (did the caller supply images?)
await initTask(retry.prompt, images?.length ? images : retry.images, files);
```