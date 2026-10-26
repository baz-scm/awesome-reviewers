---
title: Safe Lookups And Clear Boundaries
description: 'Apply two complementary security practices:


  1) Safe object map lookups for dynamic keys

  - When mapping user-controlled strings (paths, extensions, filenames, language IDs)
  to values, do not rely on plain indexing like `map[key]` alone. Use an own-property
  check so prototype-chain properties (e.g., `__proto__`, `constructor`, `toString`)
  can’t be treated as...'
repository: cline/cline#v9
label: Security
language: TSX
comments_count: 3
repository_stars: 70868
---

Apply two complementary security practices:

1) Safe object map lookups for dynamic keys
- When mapping user-controlled strings (paths, extensions, filenames, language IDs) to values, do not rely on plain indexing like `map[key]` alone. Use an own-property check so prototype-chain properties (e.g., `__proto__`, `constructor`, `toString`) can’t be treated as legitimate matches.

Example pattern:
```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: 'FileCode', className: 'text-sky-600 dark:text-sky-400' },
};

function lookupByExtension(ext: string): IconSpec {
  const key = ext.toLowerCase();
  // Prevent prototype-chain collisions
  if (Object.hasOwn(BY_EXTENSION, key)) return BY_EXTENSION[key];
  // Neutral fallback
  return { icon: 'FileText', className: 'text-muted-foreground' };
}
```
- Add/keep tests that cover keys like `__proto__`, `constructor`, and `toString`.

2) Unambiguous security boundaries in security settings/UI
- For any security-relevant setting (file access, sandboxing, command execution, write permissions), ensure the text precisely states:
  - What is permitted vs denied (e.g., “read anywhere” vs “commands can only modify within this project”).
  - Any OS-specific behavior differences (notably Windows).
  - Where actions run (e.g., background executor vs integrated terminal), so the UI doesn’t mislead users about the effective security model.

Together, these prevent both implementation pitfalls (unsafe dynamic lookups) and operational misunderstandings (unclear security guarantees).