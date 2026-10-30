---
title: Distinguish null, undefined, empty
description: Null, `undefined`, and an empty-but-present value (`""`, `[]`, `{}`)
  are not interchangeable — treat each as a distinct state and make the distinction
  explicit in both types and checks, rather than relying on truthiness or `??`.
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 71067
---

Null, `undefined`, and an empty-but-present value (`""`, `[]`, `{}`) are not interchangeable — treat each as a distinct state and make the distinction explicit in both types and checks, rather than relying on truthiness or `??`.

- Don't use `??` or truthy checks to fall back on a value that can legitimately be empty. `images ?? retry.images` kept an empty `[]` because `??` only guards against `null`/`undefined`; the fix was `images?.length ? images : retry.images`. Similarly, `callerInitialMessages === undefined` must be paired with a `.length > 0` check where an empty array and "not provided" need different handling (e.g. `readPersistedChatMessages` returning `[]` should not be treated the same as "no history requested").
- When a sentinel is needed to mean "reset to default" vs "set to this value," pick a value that can't be confused with a normal input — e.g. use an explicit `baseUrl: null` to mean "clear and fall back to the provider default," keeping `""` as a distinct, deliberate empty value.
- Keep nullable type annotations accurate to what the runtime actually does. If a function normalizes `null` but its signature still says `| undefined`, an explicit `undefined` argument will silently fall through a parameter default and produce the wrong behavior — the signature, not the call site, must be fixed to say `| null`.
- Never let a null/undefined branch fall through implicitly into the main path. If a function is expected to always populate a value (e.g. `ensureSessionPersisted` assigning `artifacts`) but can still return without doing so, that rare case should fail loudly (throw) instead of silently continuing into logic that assumes the value is present.
- Prefer modeling "only valid/defined in this state" with discriminated types instead of a loosely optional field plus a comment (e.g. `{ phase: "beforeRun", entry: "run" | "continue" }` rather than an optional `entry?` documented as "only set for `beforeRun`"). This lets the type system, not just a comment, enforce when a field can be absent.
- When a value can be conditionally absent across multiple code paths (e.g. a submodule diff that is binary, missing, or an uninitialized repo root), give each outcome (`undefined`, empty string, thrown error) one unambiguous meaning, and don't paper over distinct cases with a blanket `.catch(() => "")`.

Example of a safe fallback that accounts for an empty-but-present value:
```ts
// Wrong: [] is truthy, so ?? never falls back to retry.images
const resolvedImages = images ?? retry.images

// Right: explicitly treat an empty array as "no new images"
const resolvedImages = images?.length ? images : retry.images
```