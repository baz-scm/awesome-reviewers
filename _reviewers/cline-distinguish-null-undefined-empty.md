---
title: Distinguish null, undefined, empty
description: 'When null, undefined, and "empty" (`[]`, `""`, missing field) can each
  carry a different meaning, handle each case explicitly instead of collapsing them
  with `??`, default parameters, or truthy checks. These three states are not interchangeable:'
repository: cline/cline
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70886
---

When null, undefined, and "empty" (`[]`, `""`, missing field) can each carry a different meaning, handle each case explicitly instead of collapsing them with `??`, default parameters, or truthy checks. These three states are not interchangeable:

- `??`/`||` treat `null`, `undefined`, and falsy values the same, which breaks when the wire format uses one to mean "absent" and another to mean "empty but present." For example, protobuf decodes an omitted optional array as `[]`, not `undefined`, so `images ?? retry.images` silently discarded the fallback even when the caller sent nothing — the fix must check the actual signal (`images?.length ? images : retry.images`), not rely on nullish coalescing.
- Default parameters only trigger on `undefined`, not `null`. If a function needs `null` to mean something different from "not passed" (e.g. "explicitly withhold this option" vs "use the default"), the parameter type and default must be written to preserve that distinction (`value: T | null = defaultValue` still passes `null` through), and the signature's type annotation must match what the implementation actually accepts and normalizes.
- When a serialization/encoding layer treats `null` and omission differently (e.g. `null` decodes as "no change" while `{}` means "clear"), do not conflate the two when rewriting call sites — verify how the receiving layer actually interprets each value, and add a regression test for the "clear" case specifically.
- Use `null` deliberately as a third state (e.g. "still loading") when `undefined`/a default value would be ambiguous with "no value yet," and have callers treat that state explicitly rather than falling back to a default.

Before merging code that branches on nullability, trace each null/undefined/empty value back to where it originates (wire format, default parameter, external API) and confirm the check matches that source's actual semantics, with a test covering the edge case (e.g. empty array from a decoded optional field, or an explicit `null` clear).