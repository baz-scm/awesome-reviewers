---
title: Explicit Null Precedence
description: 'When behavior depends on nullable/optional inputs, don’t rely on implicit
  defaults or silent fallthrough. Instead: (1) normalize null/undefined/empty into
  an intentional internal representation, (2) make precedence rules explicit, and
  (3) fail fast when invariants are violated.'
repository: cline/cline#v3
label: Null Handling
language: TypeScript
comments_count: 9
repository_stars: 70863
---

When behavior depends on nullable/optional inputs, don’t rely on implicit defaults or silent fallthrough. Instead: (1) normalize null/undefined/empty into an intentional internal representation, (2) make precedence rules explicit, and (3) fail fast when invariants are violated.

How to apply:
- Normalize early: treat `null` differently from `undefined` only if you intend to; otherwise convert both to the same internal “omitted” state.
- Use type guards for overrides: only apply an override when you have the correct type and the destination field is truly “unset”.
- Encode precedence: e.g., for legacy flags, define exactly which key wins when both are present.
- Avoid “rare null-return” fallthrough: if a function is documented to assign required fields or throw, don’t continue into the replacement path when required data is still missing.
- Add tests for omission vs empty: distinguish “field omitted” from “present but empty” in protobuf/serializations.

Example (patterned after the discussed auth + legacy-flag fixes):
```ts
function applyAuthOverride(args: { api_key?: unknown }, update: { auth?: unknown }) {
  const apiKey = typeof args.api_key === "string" ? args.api_key : undefined;
  // Only override when the caller provided a real key AND auth wasn’t already set.
  if (apiKey?.trim() && update.auth === undefined) {
    update.auth = { accessToken: "", refreshToken: "" };
  }
}

function isDisabled(frontmatter: Record<string, unknown>): boolean {
  // Precedence: disabled wins; enabled:false only applies when disabled is absent.
  if (typeof frontmatter.disabled === "boolean") return frontmatter.disabled;
  return frontmatter.enabled === false;
}
```

This prevents silent “wrong branch” behavior like stale credentials winning over new inputs, incorrect retry attachment inheritance, or SQL/logic paths breaking because values effectively became NULL.