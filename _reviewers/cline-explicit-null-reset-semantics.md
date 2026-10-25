---
title: Explicit Null Reset Semantics
description: Null/undefined handling must preserve intent across API boundaries and
  persistence layers. Treat `undefined` as “not provided/unchanged/omit”, and treat
  `null` (or an explicitly reset payload) as “clear/reset this value”. Ensure your
  type annotations and runtime normalization match what the receiving contract/storage
  layer expects, and lock the behavior...
repository: CLINE/cline
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70839
---

Null/undefined handling must preserve intent across API boundaries and persistence layers. Treat `undefined` as “not provided/unchanged/omit”, and treat `null` (or an explicitly reset payload) as “clear/reset this value”. Ensure your type annotations and runtime normalization match what the receiving contract/storage layer expects, and lock the behavior with tests for clear/reset vs default transitions.

Apply:
- **For “clear/reset” actions:** send the contract’s expected reset representation (often explicit `null` or a specific empty object/shape), not `{}` accidentally, and not an omitted field.
- **For “update/replace” actions:** send the field only when you truly mean to change it; otherwise omit with `undefined`.
- **For `null` vs `undefined`:** if code or defaults treat them differently (e.g., `null` should not be swallowed like `undefined`), ensure the function signature and call sites agree.
- **For “empty vs absent” collections/strings:** distinguish between “caller provided empty” and “caller omitted”. Don’t assume protobuf/RPC decoding preserves omissions; handle decoded defaults intentionally.

Example pattern (clear vs omit):
```ts
// clear/reset vs omit
const payload = {
  // If user cleared a field, send explicit reset value the contract expects:
  baseUrl: userCleared ? null : undefined, // undefined => omit/leave unchanged
};

// persistence: match the storage encoding expected for clears
await client.command("session.update", {
  sessionId,
  ...(metadataToClear ? { metadata: {} } : { metadata: updates.metadata }),
});
```

Also add focused tests for:
- custom→default (cleared) transitions
- “clear” becoming a no-op due to `null` being decoded as omitted
- cases where omitted fields decode to defaults (e.g., protobuf `images` -> `[]`) and must not overwrite previous values unintentionally.