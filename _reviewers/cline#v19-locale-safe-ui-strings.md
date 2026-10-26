---
title: Locale-Safe UI Strings
description: 'When writing UI code, treat user-facing text and interactive controls
  as part of code style:


  - Don’t hardcode punctuation or English word order when composing sentences/lists.
  Translate each meaningful fragment and use locale-aware joining (e.g., Intl.ListFormat)
  so languages like Korean/Chinese don’t end up with incorrect separators.'
repository: cline/cline#v19
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70885
---

When writing UI code, treat user-facing text and interactive controls as part of code style:

- Don’t hardcode punctuation or English word order when composing sentences/lists. Translate each meaningful fragment and use locale-aware joining (e.g., Intl.ListFormat) so languages like Korean/Chinese don’t end up with incorrect separators.
- Use correct semantic elements for interactivity (e.g., prefer `<button type="button">` over `<a role="button">` or click-only anchors) so keyboard behavior is correct by default.
- Prefer shared UI primitives (icons/components) when available to keep behavior and rendering consistent and easy to audit.

Example (locale-safe composition):
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t('chatView:toolGroup.files', { count: counts.read }));
if (counts.search > 0) parts.push(t('chatView:toolGroup.performedSearches', { count: counts.search }));

if (parts.length === 0) return t('chatView:toolGroup.contextFallback');

const items = new Intl.ListFormat(currentLocale, { style: 'long', type: 'conjunction' }).format(parts);
return t('chatView:toolGroup.summary', { items });
```

Checklist: any UI string built with manual commas must be reviewed for locale correctness; any interactive UI must be a semantically correct element.