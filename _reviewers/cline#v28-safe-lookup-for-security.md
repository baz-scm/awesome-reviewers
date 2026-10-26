---
title: Safe Lookup For Security
description: When security-relevant behavior depends on externally derived strings
  (paths, extensions, filenames, setting-driven permission boundaries), prevent prototype-chain
  surprises and ensure the UI text precisely matches what’s enforced.
repository: cline/cline#v28
label: Security
language: TSX
comments_count: 3
repository_stars: 70893
---

When security-relevant behavior depends on externally derived strings (paths, extensions, filenames, setting-driven permission boundaries), prevent prototype-chain surprises and ensure the UI text precisely matches what’s enforced.

Apply this in two ways:

1) Safe lookup for map keys
- If you use plain objects as lookup tables (e.g., extension -> language, filename -> icon), only accept own properties.
- Prefer `Object.hasOwn(map, key)` (or a null-prototype object) instead of trusting `map[key]` alone.
- Add tests that cover `__proto__`, `constructor`, and similar keys.

Example pattern:

```ts
type Spec = { value: string };
const BY_EXT: Record<string, Spec> = {
  ts: { value: "TypeScript" },
  json: { value: "JSON" },
};

export function safeSpecForExtension(ext: string): Spec {
  // ext may come from a user-controlled path/filename
  if (Object.hasOwn(BY_EXT, ext)) return BY_EXT[ext];
  return { value: "Neutral" };
}
```

2) Make permission/execution boundaries unambiguous
- Security setting copy must clearly distinguish what is allowed (read vs write/mutate) and where/which component executes commands (e.g., background executor vs integrated terminal).
- Verify wording across platforms (e.g., Windows sandbox differences) so users understand the real enforcement model.

Outcome: fewer security edge cases from prototype-chain key handling and fewer user misunderstandings about what the system will actually permit or change.