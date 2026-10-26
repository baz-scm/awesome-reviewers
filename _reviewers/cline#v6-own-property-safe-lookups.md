---
title: Own-property safe lookups
description: When using object/dictionary tables for security-relevant decisions (e.g.,
  extension→language/icon, path/name→handlers), do not rely on prototype-chain lookups.
  Use an own-property check (Object.hasOwn or a null-prototype map), and always fall
  back to a safe default for unknown/invalid keys. Add tests that cover prototype-chain
  keys (constructor, __proto__,...
repository: cline/cline#v6
label: Security
language: TSX
comments_count: 3
repository_stars: 70864
---

When using object/dictionary tables for security-relevant decisions (e.g., extension→language/icon, path/name→handlers), do not rely on prototype-chain lookups. Use an own-property check (Object.hasOwn or a null-prototype map), and always fall back to a safe default for unknown/invalid keys. Add tests that cover prototype-chain keys (constructor, __proto__, toString).

Also, for security boundary settings, ensure user-facing descriptions are unambiguous about what’s allowed (read vs write) and which execution path is constrained (e.g., background executor vs terminal).

Example (own-property mapping with safe fallback):

```ts
type Spec = { icon: unknown; className: string };

const BY_EXTENSION: Record<string, Spec> = {
  ts: { icon: 'CODE', className: 'text-sky-600 dark:text-sky-400' },
};

function safeLookup(map: Record<string, Spec>, key: string, fallback: Spec): Spec {
  return Object.hasOwn(map, key) ? map[key] : fallback;
}

export function languageForPath(path: string): string {
  const name = path.split(/[\\/]/).pop() ?? path;
  const extension = name.includes('.') ? (name.split('.').pop() ?? '').toLowerCase() : '';

  const fallback = extension; // or 'text/plain'
  const EXTENSION_LANGUAGES: Record<string, string> = { ts: 'typescript' };
  return Object.hasOwn(EXTENSION_LANGUAGES, extension) ? EXTENSION_LANGUAGES[extension] : fallback;
}
```

Test guidance:
- Include cases like `languageForPath('__proto__')`, `languageForPath('constructor')`, and `languageForPath('toString')` to ensure they don’t resolve to mapped values.
- For security settings: explicitly state read vs write scope and affected executor/terminal in the UI text.