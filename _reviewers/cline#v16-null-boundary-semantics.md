---
title: Null boundary semantics
description: 'Adopt a single rule for nullable values: at API boundaries, treat `undefined`
  (omit/keep current) and `null` (explicitly clear/reset) as distinct intent states,
  then normalize once so the rest of the code can’t accidentally conflate them.'
repository: cline/cline#v16
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 70882
---

Adopt a single rule for nullable values: at API boundaries, treat `undefined` (omit/keep current) and `null` (explicitly clear/reset) as distinct intent states, then normalize once so the rest of the code can’t accidentally conflate them.

Practical checklist:
1) Make reset semantics explicit in the wire/contract layer.
   - If the user clears a value (e.g., custom base URL), send the explicit reset so the recipient can distinguish it from “field not provided”.
2) Keep schemas “truthful”, but normalize runtime inputs.
   - Prefer non-null types in schemas and normalize `null` to omission where the operation is supposed to create/insert without replacements.
3) Preserve intent when upstream decodes defaults.
   - Protocol/serialization may turn omitted fields into empty arrays/zero values; treat “empty decoded” as “not provided” when that’s the intent.
4) Be defensive with optional gating data.
   - If behavior depends on optional auth/config facts, don’t silently fall through to a false negative when those facts are missing or mismatched—either treat it as “unknown” or request the needed facts.
5) Prevent accidental NULL propagation from external systems.
   - Ensure you use the exact parameter names/shape required by the external layer (e.g., sqlite named parameters) so they don’t bind as NULL.

Example pattern (schema + normalization):
```ts
// Schema advertises only non-null for create/insert replacement edits.
const ReplaceTextSchema = z.object({
  path: z.string().min(1),
  old_text: z.string().min(1),
  new_text: z.string().min(1),
});

function normalizeEdits(input: unknown) {
  const parsed = ReplaceTextSchema.safeParse(input);
  if (!parsed.success) throw parsed.error;

  // If some models send null for fields that are unused, normalize by omission.
  // (undefined means “keep current / treat as not provided”.)
  return {
    ...parsed.data,
    // e.g. for replace/insert operations:
    // new_text: parsed.data.new_text === null ? undefined : parsed.data.new_text
  };
}
```

Apply this consistently: normalize `null`/`undefined` at the boundary (UI → controller, controller → session/connection, config building, DB/protocol calls) so inner logic can rely on unambiguous intent.