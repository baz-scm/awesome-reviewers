---
title: Null and Omission Semantics
description: When code crosses process/contract boundaries (RPC/protocol/serialization/UI-state
  syncing), treat `null`, `undefined`/omitted fields, and empty literals (`""`, `[]`,
  `{}`) as distinct semantics—and ensure both sender and receiver implement the same
  meaning. Don’t rely on `??`/truthiness or silent fallthrough to “do the right thing”.
repository: cline/cline#x
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 70861
---

When code crosses process/contract boundaries (RPC/protocol/serialization/UI-state syncing), treat `null`, `undefined`/omitted fields, and empty literals (`""`, `[]`, `{}`) as distinct semantics—and ensure both sender and receiver implement the same meaning. Don’t rely on `??`/truthiness or silent fallthrough to “do the right thing”.

Apply this checklist:
- **Match downstream meaning:** If the receiver distinguishes `null` vs omitted, send `null` explicitly and decode it accordingly.
- **Avoid `??` with arrays/optionals:** Protocols may decode omitted fields as empty arrays; use conditional logic that detects whether the field was actually provided.
- **Make “unknown/missing context” explicit:** If optional auth/provider context affects error classification or capability checks, handle “missing” as a deliberate state (e.g., alternate error/action), not as an accidental default.
- **Encode conditional presence in types:** Prefer discriminated unions/explicit state shapes (compile-time) over runtime “maybe set” fields.
- **Regression test the transitions:** Add tests for clear-to-default, `null`-clear behavior, and retry/omitted-field behaviors.

Example patterns:

1) Correctly distinguish “clear” vs “not set” in updates
```ts
// If clearing must be observed as a real clear, encode it explicitly.
await sessionUpdate({ baseUrl: null });

// Avoid changing null->omitted encoding unless the persistence semantics match.
```

2) Don’t confuse omitted `images` with `[]`
```ts
async function maybeUseRetryImages(args: {
  images?: string[]; // could be omitted and decode to []
  retryImages: string[];
}) {
  // Only use retry images when the response truly did not carry an images field.
  const images = args.images;
  const hasImagesField = images !== undefined; // adjust to your transport semantics
  return hasImagesField ? images : args.retryImages;
}
```

3) Prefer type-safe conditional fields
```ts
type BeforeRun = { entry: 'beforeRun'; snapshotExtra: string };
type NotBeforeRun = { entry: 'run' | 'continue' };

type Context = BeforeRun | NotBeforeRun;

function handle(ctx: Context) {
  if (ctx.entry === 'beforeRun') {
    // ctx.snapshotExtra is available here
  }
}
```

Using this standard prevents regressions where `null` clears don’t clear, omitted fields unexpectedly become empty arrays, or missing optional context silently routes users into the wrong failure state.