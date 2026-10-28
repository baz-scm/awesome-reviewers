---
title: Null vs undefined semantics
description: 'Treat `null`, `undefined`, and "key omitted" as distinct states, especially
  at serialization boundaries (protobuf, JSON, RPC payloads) and in parameter defaults
  — collapsing them silently changes behavior. Before using `??`, default parameters,
  or spreading an object to drop a key, verify what each of null/undefined/empty actually
  means for the callee:'
repository: cline/cline?x
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70983
---

Treat `null`, `undefined`, and "key omitted" as distinct states, especially at serialization boundaries (protobuf, JSON, RPC payloads) and in parameter defaults — collapsing them silently changes behavior. Before using `??`, default parameters, or spreading an object to drop a key, verify what each of null/undefined/empty actually means for the callee:

- A default parameter swallows `undefined` but not `null`; if your API needs to tell "caller said nothing" from "caller explicitly disabled this," the type must allow `null` explicitly and the signature must say so (don't annotate `| undefined` while the body normalizes `null`).
- An intentional `null` meant to "clear" a field can get encoded as an omitted key by a generic serializer (e.g. a `asPlainRecord`-style decoder that treats `null` as absent), silently turning a clear into a no-op. When a field supports an explicit clear, encode that case deliberately (e.g. send `{}` or a dedicated sentinel) and add a regression test for it instead of relying on default object spreading.
- `??` only catches `null`/`undefined` — it does not catch a present-but-empty value such as `[]` that a protocol decodes for an omitted field. If "empty" and "absent" need different handling, check emptiness explicitly:

```ts
// Wrong: [] from the decoder is not null/undefined, so retry.images is lost
const images = incoming ?? retry.images;

// Right: treat empty array as "nothing new", fall back explicitly
const images = incoming?.length ? incoming : retry.images;
```

- When a field is advertised to external callers (schemas, APIs) that may send `null` for "unused," accept `null` at the boundary but normalize it to omission internally, and document why — rather than relying on implicit type coercion.
- When falling back across optional/nullable fields in matching logic (e.g. `config.providerAuth?.providerId === config.provider`), make sure the fallback path still fails loud when the match can't be made, rather than silently skipping a check that should run.

Always add a test for each boundary case — explicit `null`, `undefined`, omitted key, and empty collection — whenever one of these states carries distinct meaning.