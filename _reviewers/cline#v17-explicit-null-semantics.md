---
title: Explicit Null Semantics
description: When handling optional/nullable inputs, make the meaning of `undefined`,
  `null`, and “empty” (e.g., `[]`) explicit, and ensure both your runtime normalization
  and TypeScript/Zod types encode that intent.
repository: cline/cline#v17
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70883
---

When handling optional/nullable inputs, make the meaning of `undefined`, `null`, and “empty” (e.g., `[]`) explicit, and ensure both your runtime normalization and TypeScript/Zod types encode that intent.

Practical rules:
- **Constrain invariants in the schema** (e.g., non-empty arrays) so failures are meaningful and not incidental (like union mismatch).
- **Define field precedence** when multiple properties represent the same decision, and implement the same precedence everywhere (e.g., `disabled` wins; legacy `enabled: false` only applies when `disabled` is absent).
- **Never default based only on presence if the empty value is semantically meaningful.** In particular, don’t treat protobuf/serialization “omitted” fields as equivalent to an explicitly provided empty array—check for “empty vs non-empty” rather than just `undefined`.
- **Align types with normalization.** If code normalizes `null` to something else, the function signature must reflect `null` (and not just `undefined`) so the compiler enforces the same contract.
- **Prefer type-driven design or construction-time initialization** to reduce nullable state branching.

Example patterns:

1) Avoid confusing omitted vs empty arrays (retry attachments)
```ts
// Bad: omitted protobuf images may decode to []
// images ?? retry.images

// Good: treat empty list as intentional-webview-empty; otherwise fall back to retry's attachments
const effectiveImages = images?.length ? images : retry.images;
await initTask(retry.prompt, effectiveImages, files, undefined, undefined, retry.cloudTarget);
```

2) Enforce non-empty arrays via schema
```ts
const Schema = z.array(ItemSchema).min(1);
```

3) Ensure signature matches normalization (`null` vs `undefined`)
```ts
function resolve(req: GatewayStreamRequest, context?: Context | null) {
  // If the implementation treats null specially, the type must too.
}
```

Applying this consistently prevents subtle fallback bugs, incorrect precedence, and “null safety” that only exists at runtime but not in the type system.