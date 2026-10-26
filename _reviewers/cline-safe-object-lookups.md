---
title: Safe object lookups
description: When you build “string key → meaning” maps from paths, extensions, plugin
  data, or other user-influenced strings, never rely on inherited object members.
  Use own-property checks (e.g., `Object.hasOwn`) and ensure the same normalization
  is applied wherever the key is produced and later consumed. For security-related
  toggles, the UI text must precisely...
repository: Cline/Cline
label: Security
language: TSX
comments_count: 4
repository_stars: 70840
---

When you build “string key → meaning” maps from paths, extensions, plugin data, or other user-influenced strings, never rely on inherited object members. Use own-property checks (e.g., `Object.hasOwn`) and ensure the same normalization is applied wherever the key is produced and later consumed. For security-related toggles, the UI text must precisely describe what is allowed (read vs command/write) and where commands actually run.

Example (safe lookup + normalized key):
```ts
type IconSpec = { /* ... */ };
const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { /* ... */ },
  // ...
};

function baseName(path: string) {
  return path.split(/[\\/]/).pop() ?? path;
}

export function iconForPath(path: string): IconSpec | undefined {
  const name = baseName(path).toLowerCase();
  const ext = name.includes('.') ? name.split('.').pop()?.toLowerCase() ?? '' : '';

  // Prevent inherited-property lookups like __proto__/constructor.
  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];
  return undefined; // neutral fallback
}

// When matching dispatch paths/menus:
// normalize the same way before registration/inspection/execution (e.g., trim).
const normalizedMenuPath = menuPath.trim();
```
Apply this specifically to dictionary-style tables used for: icon/language detection, handler resolution, command dispatch, and any lookup keyed by external strings.