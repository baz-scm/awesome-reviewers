---
title: Safe Lookup and Permission Clarity
description: 'Use secure patterns whenever untrusted strings or security-sensitive
  policies are involved:


  1) Prototype-safe lookup maps

  - If you map a derived string (e.g., path basename/extension) to metadata via an
  object literal, ensure you only accept own properties—never inherited Object members.'
repository: cline/cline#v20
label: Security
language: TSX
comments_count: 3
repository_stars: 70886
---

Use secure patterns whenever untrusted strings or security-sensitive policies are involved:

1) Prototype-safe lookup maps
- If you map a derived string (e.g., path basename/extension) to metadata via an object literal, ensure you only accept own properties—never inherited Object members.
- Apply this even if the map is “just UI data” (icons/language highlighting), because inherited keys like `__proto__` / `constructor` can be used to alter control flow or render unexpected content.
- Add tests for edge keys.

Example pattern:
```ts
type Spec = { value: string };
const MAP: Record<string, Spec> = {
  ts: { value: "TypeScript" },
};

export function safeLookup(key: string): Spec | undefined {
  return Object.hasOwn(MAP, key) ? MAP[key] : undefined;
}
```

(Alternative: `const MAP = Object.create(null) as Record<string, Spec>;` then use `MAP[key] !== undefined`, but keep tests for `__proto__`/`constructor`.)

2) Precise permission/sandbox messaging
- When describing settings that affect authorization or sandbox boundaries, ensure the text matches the actual enforced filesystem policy (including OS-specific differences) and clearly separates:
  - what is allowed to *read* vs what is allowed to *modify*
  - what commands can do vs what tools can do
  - where actions run (e.g., background executor vs integrated terminal)
- Ambiguous UI copy is a security issue because it can cause users to misconfigure trust/aut-approval.

Checklist for PRs
- Do map lookups derived from paths/strings use an own-property check (or null-prototype map) and have tests for `__proto__` and `constructor`?
- Do user-facing setting descriptions accurately reflect the real enforcement boundaries (read vs write, project vs full machine, command execution context)?