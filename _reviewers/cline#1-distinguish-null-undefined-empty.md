---
title: Distinguish null, undefined, empty
description: Several bugs came from treating "no value" as a single undifferentiated
  concept when the system actually has multiple distinct absence states (undefined
  = not provided/use default, null = explicitly cleared/unknown, empty string/array
  = a real but empty value). Each meaning must be modeled and checked explicitly,
  not conflated via a generic falsy/nullish...
repository: cline/cline#1
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 71024
---

Several bugs came from treating "no value" as a single undifferentiated concept when the system actually has multiple distinct absence states (undefined = not provided/use default, null = explicitly cleared/unknown, empty string/array = a real but empty value). Each meaning must be modeled and checked explicitly, not conflated via a generic falsy/nullish check.

Guidelines:
- Before using `??` or `||` as a fallback, verify what the producer actually sends for "nothing". Protobuf/JSON often decode an omitted field as `[]` or `""`, not `null`/`undefined`, so `images ?? retry.images` silently keeps an empty array instead of falling back — check `images?.length ? images : retry.images` instead.
- When a value can be cleared back to a provider/manifest default, send an explicit `null` as the "reset" signal and keep `""` as a distinct, intentional empty value; don't let an empty string and "no override" collapse into the same case.
- If `undefined` triggers a parameter default you don't want, use `null` deliberately for "explicitly withheld" and make sure the function signature's type (`T | null` vs `T | undefined`) matches what the implementation actually checks — a signature/implementation mismatch here is a silent bug, not just a type nit.
- When a field is only meaningful in some states (e.g. `entry` only set during `beforeRun`), prefer a discriminated union (`{ phase: "beforeRun"; entry: "run" | "continue" } | { phase: "continue" }`) over leaving it `optional`/`undefined` everywhere else, so the type system enforces when it's safe to read.
- When an external input (API response, third-party model) can send `null` for different reasons (e.g., one caller means "no value", another means "unused optional"), normalize it explicitly at the boundary and document why, rather than accepting it implicitly through a loosened schema.
- Never silently fall through on an unexpected `null`/`undefined` in a path meant to guard against it (e.g., an invariant that "this is always set by now"); throw or assert instead so the bug surfaces immediately rather than re-entering a now-broken code path.

Example:
```ts
// Bad: assumes "no images" is always null/undefined
await initTask(retry.prompt, images ?? retry.images, files)

// Good: accounts for the empty-array sentinel the webview actually sends
await initTask(retry.prompt, images?.length ? images : retry.images, files)
```