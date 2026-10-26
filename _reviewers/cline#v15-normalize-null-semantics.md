---
title: Normalize Null Semantics
description: Null/undefined handling should be explicit and consistent at system boundaries.
  Treat `null` vs “omitted” as distinct unless you can prove they mean the same thing
  end-to-end.
repository: cline/cline#v15
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 70877
---

Null/undefined handling should be explicit and consistent at system boundaries. Treat `null` vs “omitted” as distinct unless you can prove they mean the same thing end-to-end.

**Coding standards**
1. **Normalize early at boundaries**: If upstream providers/protocols send `null` where your domain expects “absent”, convert `null` to omission/`undefined` (or the correct domain value) *immediately*.
2. **Preserve semantics across persistence/transport**: Do not refactor encoding such that `null` becomes `{}` (or vice versa) unless the downstream layer treats them identically. Add/keep tests that assert the meaning of “clear”, “update”, and “no-op”.
3. **Prevent accidental NULL propagation to external systems**: For SQL/DB bindings and other FFI/protocol layers, ensure “missing” doesn’t get interpreted as SQL `NULL` due to token/name mismatches.
4. **Use TypeScript to model presence when practical**: When “only set for X” matters, prefer union/shape types so invalid states are unrepresentable rather than guarded by ad-hoc `if` checks.

**Example: normalize `null` to omission**
```ts
type ReplacementEdit = {
  old_text?: string; // absent means omitted
};

function normalizeReplacementEdit(input: {
  old_text?: string | null;
}): ReplacementEdit {
  return {
    ...(input.old_text == null ? {} : { old_text: input.old_text }),
  };
}
```

**Example: keep “clear” semantics stable**
- If your persistence layer distinguishes `{}` (clear) from omission, ensure callers never change `null` encoding to `{}` (or the reverse) without updating tests for the exact behavior.

**Test rule of thumb**
- Add tests that cover: (a) field omitted, (b) field set to `null`, (c) field set to a value—verifying the resulting persisted/DB state matches the intended semantics.