---
title: Prototype-Safe Mappings
description: 'When you map user-controlled strings (file paths, extensions, names)
  to security-relevant behavior or UI state, do two things:

  1) **Defend lookups against prototype-chain keys**: use an own-property check (e.g.,
  `Object.hasOwn`) before indexing into lookup tables, and provide a neutral default.'
repository: cline/cline#x
label: Security
language: TSX
comments_count: 3
repository_stars: 70861
---

When you map user-controlled strings (file paths, extensions, names) to security-relevant behavior or UI state, do two things:
1) **Defend lookups against prototype-chain keys**: use an own-property check (e.g., `Object.hasOwn`) before indexing into lookup tables, and provide a neutral default.
2) **Keep capability boundaries explicit**: if settings constrain access (e.g., read allowed broadly, write restricted to a project), ensure both the implementation and the UI text clearly distinguish what’s permitted and where commands run.

Example (prototype-safe dictionary lookup):
```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = { /* ... */ };

export function safeLookupExtension(path: string): IconSpec | undefined {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";

  // Prevent prototype-chain surprises (e.g., __proto__, constructor, toString)
  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];

  return undefined; // or a neutral default icon spec
}
```

Also ensure security settings copy is unambiguous (e.g., “commands can only change files in this project” vs “the tool can read elsewhere”), and mention the execution context (background executor vs integrated terminal) when it affects user expectations of safety or control.

Add/maintain tests for edge keys like `__proto__`, `constructor`, and unusual extensions/filenames, plus tests that verify the expected fallback behavior.