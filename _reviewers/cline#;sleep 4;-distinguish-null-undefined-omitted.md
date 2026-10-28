---
title: Distinguish null, undefined, omitted
description: Null and undefined are not interchangeable — treat them as distinct signals
  (explicit reset/clear, explicit "none", vs. "not provided/leave unchanged") and
  make that distinction visible in both types and runtime checks, especially at external
  boundaries (RPC responses, provider APIs, protobuf-decoded fields) where values
  arrive untyped or coerced.
repository: cline/cline#;sleep 4;
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70976
---

Null and undefined are not interchangeable — treat them as distinct signals (explicit reset/clear, explicit "none", vs. "not provided/leave unchanged") and make that distinction visible in both types and runtime checks, especially at external boundaries (RPC responses, provider APIs, protobuf-decoded fields) where values arrive untyped or coerced.

Concretely:
- Never assume an external value narrows to the type you expect. Validate/narrow explicitly instead of relying on `!== undefined` or truthiness checks. For example, a paging cursor from an untrusted server may come back as `null` instead of `undefined`; a loose check (`cursor !== undefined`) will treat `null` as "more pages" and loop forever. Narrow explicitly: `cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined;`
- When `null` and `undefined` must mean different things (e.g. "explicitly clear this field" vs "field not supplied, leave as-is"), encode and test that difference end-to-end. Don't let an intermediate layer collapse one into the other — e.g. sending `metadata: null` to clear a record must not become `{}` (no-op) or vice versa; keep the encoding that preserves the clear semantics and add a regression test for it.
- Be careful with default parameters: `foo = someValue ?? defaultValue` silently swallows `undefined`, so if `null` needs to reach the implementation to signal "no value" distinctly from "use default," the function signature must declare `| null` explicitly (not just `| undefined`), and call sites must pass the right one.
- Prefer modeling "this field only applies in certain states" with discriminated types rather than a loosely-optional field plus a comment (e.g. instead of documenting "only set for `beforeRun`", use a tagged union like `{ phase: "beforeRun"; entry: "run" | "continue" } | { phase: "afterRun" }`) so the compiler enforces correct usage instead of relying on comments.
- If a value is nearly always present, avoid the overhead and optionality of lazily-initialized nullable state; initialize it eagerly (e.g. in a constructor) and make the type non-nullable, removing unnecessary `?`/conditional checks downstream.
- At schema boundaries, when a model or client sends `null` for a field that should logically be a string, decide and document whether `null` is normalized to "omitted" at runtime, and keep that normalization generic rather than naming specific callers that may change over time.</description>
</invoke>
