---
title: Distinguish null semantics precisely
description: 'Several bugs came from conflating different "absence" states — missing,
  empty, loading, explicitly cleared, or unreadable — when they carry different meanings
  and require different handling. Guard against this by:'
repository: cline/cline?foo=bar
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 71082
---

Several bugs came from conflating different "absence" states — missing, empty, loading, explicitly cleared, or unreadable — when they carry different meanings and require different handling. Guard against this by:

1. Never substitute a loose fallback (`??`, truthy checks, `.length`) when the distinction between `null`, `undefined`, and an empty collection/string matters. For example, an empty array result from "no stored messages" must not be treated the same as "no result requested" (`initialMessages.length > 0`, not just presence), and a missing config file must be distinguished from one that exists but failed to read (return a distinct "unknown" rather than silently empty).

2. Keep type annotations exactly in sync with runtime behavior. If a function's body normalizes or depends on `null` versus `undefined`, the signature must say so explicitly (`T | null`, not `T | undefined`) — a mismatch lets a default-parameter swallow an `undefined` that should have been a meaningful `null`, silently changing behavior.

3. When representing state that's only meaningful in certain cases (e.g., "this field is only set for `beforeRun`", "this value is `null` only while loading"), prefer encoding that as a discriminated union or distinct type rather than a loosely-optional field with a comment — let the compiler enforce where the value can legitimately be absent.

4. Treat an "impossible" null/undefined branch from a function that is documented to always assign-or-throw as a real failure path: throw explicitly rather than falling through into logic that assumes the value is present, which can otherwise cause silent corruption (e.g., orphaning a live session).

5. When a value needs to represent "explicitly cleared" (e.g., resetting a custom base URL), use an explicit `null`/sentinel reset distinct from an empty string or omission, so downstream consumers can tell "reset to default" apart from "set to empty".

Applying these practices prevents silent fallthroughs, mismatched optional/nullable types, and ambiguous "empty" semantics that produce hard-to-reproduce bugs.