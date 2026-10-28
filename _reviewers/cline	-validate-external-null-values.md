---
title: Validate external null values
description: When consuming values from external or semi-trusted sources (network/RPC
  responses, deserialized protocols, model-generated tool calls), never assume "no
  value" only ever shows up as `undefined`. Protocols and callers can represent absence
  as `null`, an empty string, or an empty array, and a strict `=== undefined` check
  or a bare `??` fallback will silently...
repository: "cline/cline\t"
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 70947
---

When consuming values from external or semi-trusted sources (network/RPC responses, deserialized protocols, model-generated tool calls), never assume "no value" only ever shows up as `undefined`. Protocols and callers can represent absence as `null`, an empty string, or an empty array, and a strict `=== undefined` check or a bare `??` fallback will silently miss those cases, producing subtle bugs (infinite pagination loops, dropped attachments, schema validation rejecting valid input).

Explicitly narrow and normalize these values at the boundary instead of relying on identity comparisons:

```ts
// Bad: only catches the exact `undefined` case; a server sending
// `nextCursor: null` makes `null !== undefined` true forever.
cursor = result.nextCursor;

// Good: narrow to the expected type and normalize anything else to "no value".
cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined;
```

```ts
// Bad: protobuf decodes an omitted `images` field as `[]`, not `undefined`,
// so `??` never falls back to the previous value.
const nextImages = images ?? retry.images;

// Good: treat "empty" the same as "absent".
const nextImages = images?.length ? images : retry.images;
```

The same applies when designing schemas consumed by external producers (e.g. LLM tool calls): if a field must never be `null`, advertise only the valid type in the schema, but still accept `null` at the parsing boundary and normalize it to the omitted/undefined case, rather than letting it flow through as a real value or rejecting a request that is otherwise valid. Apply this check wherever a value crosses a trust boundary (network, IPC, protocol buffers, user/model input) before using it in control flow.