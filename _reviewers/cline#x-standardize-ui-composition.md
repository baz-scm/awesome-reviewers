---
title: Standardize UI Composition
description: When adding or changing UI, avoid ad-hoc string/layout/icon composition
  that breaks in edge cases. Use shared, standardized patterns for (a) responsive
  layout, (b) locale-safe text, and (c) consistent UI primitives.
repository: cline/cline#x
label: Code Style
language: TSX
comments_count: 4
repository_stars: 70861
---

When adding or changing UI, avoid ad-hoc string/layout/icon composition that breaks in edge cases. Use shared, standardized patterns for (a) responsive layout, (b) locale-safe text, and (c) consistent UI primitives.

Apply these rules:
1) Responsive layout: for drawers/tabs/modals, prefer sizing rules that keep controls reachable (e.g., viewport-capped height + scroll; flex shrink + truncation instead of overflow containers that clip “attached” effects).
2) Locale-safe text: don’t hardcode English word order or manual separators. Build each segment as a self-contained phrase and join via `Intl.ListFormat` (or equivalent per-locale utilities). Always include a fallback when there’s no content.
3) Consistent primitives: reuse the same icon/component import conventions used elsewhere so icon usage is easy to audit.

Example (locale-safe join):
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t('chatView:toolGroup.files', { count: counts.read }));
if (parts.length === 0) return t('chatView:toolGroup.contextFallback');
const items = new Intl.ListFormat(locale, { style: 'long', type: 'conjunction' }).format(parts);
return t('chatView:toolGroup.summary', { items });
```

Example (viewport-capped dialog):
- Use something like `max-h-[calc(100dvh-2rem)]` and `overflow-auto` so primary actions remain clickable on short windows.