---
title: Safe Own-Property Lookups
description: Any time code turns untrusted input (paths, filenames, extensions, identifiers)
  into a decision via an in-memory lookup table, ensure the lookup only matches *own*
  properties. This prevents inherited keys like `__proto__`, `constructor`, `toString`,
  etc. from altering behavior.
repository: cline/cline#v23
label: Security
language: TSX
comments_count: 3
repository_stars: 70889
---

Any time code turns untrusted input (paths, filenames, extensions, identifiers) into a decision via an in-memory lookup table, ensure the lookup only matches *own* properties. This prevents inherited keys like `__proto__`, `constructor`, `toString`, etc. from altering behavior.

Apply this especially to security-relevant UI/behavior (e.g., interpreting file paths to decide rendering, highlighters, or capabilities), and keep security setting text unambiguous about what is allowed (read vs modify/scope, and where commands execute).

Example (pattern):

```ts
type IconSpec = { icon: unknown; className: string };
const BY_NAME: Record<string, IconSpec> = {
  "package.json": { icon: {}, className: "text-red-600" },
};

function baseName(p: string) {
  return p.split(/[\\/]/).pop() ?? p;
}

export function iconSpecFromPath(path: string): IconSpec {
  const name = baseName(path).toLowerCase();
  if (Object.hasOwn(BY_NAME, name)) return BY_NAME[name];
  return { icon: {}, className: "text-muted-foreground" }; // neutral fallback
}
```

Also, when documenting or labeling security controls, explicitly state scope differences (e.g., “commands can only change files in this project” vs “files can be read elsewhere”) and execution context (e.g., background executor vs integrated terminal), so users don’t make unsafe assumptions.