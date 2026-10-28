---
title: Null vs undefined semantics
description: Treat `null`, `undefined`, and "empty-but-present" (e.g. `""`, `[]`,
  `{}`) as distinct states, and make the code that consumes them reflect that distinction
  instead of collapsing them with loose checks like `??`, `||`, or a bare `!== undefined`.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 70984
---

Treat `null`, `undefined`, and "empty-but-present" (e.g. `""`, `[]`, `{}`) as distinct states, and make the code that consumes them reflect that distinction instead of collapsing them with loose checks like `??`, `||`, or a bare `!== undefined`.

Concrete guidance:
- When validating external/untrusted input (another process, a model, an API response), explicitly narrow to the expected type rather than trusting the shape. A server returning `nextCursor: null` should not satisfy a `!== undefined` pagination check: `cursor = typeof result.nextCursor === "string" ? result.nextCursor : undefined`.
- Don't use `??` to pick between "caller supplied nothing" and "caller supplied an empty value" when the empty value is meaningful. `images ?? retry.images` keeps `[]` (a real, if empty, value) instead of falling back; prefer an explicit check such as `images?.length ? images : retry.images`.
- When `null` is used as a sentinel for "clear this field," preserve that encoding end-to-end. Folding `metadata: null` into a generic merge turned an intentional clear into a no-op; keep `null`, `{}` (clear), and omitted (`undefined`, keep existing) as three distinct wire values if the receiving layer distinguishes them.
- Use `null`/`undefined` to represent genuinely different states (e.g. "still loading" vs "nothing saved") rather than reusing one default value for both, so downstream consumers can render the right thing (disabled/loading vs a concrete default).
- Avoid broad `catch`/fallback blocks that squash distinct outcomes (missing path, wrong kind of object, real I/O error) into the same `null`/empty result; only swallow the specific case you intend to treat as absent, and let other errors and flags (e.g. `truncated`, `binary`) propagate.
- When a function is expected to always produce a non-null result after some step (e.g. `ensureSessionPersisted`), don't silently fall through on the rare `null` case — throw or handle it explicitly so the invariant violation surfaces instead of being masked.

Applying these checks during review catches an entire class of bugs where a value that is "present but empty" or "explicitly cleared" is silently treated the same as "missing."