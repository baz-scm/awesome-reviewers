---
title: Localized summaries & native controls
description: 'When composing user-facing text and interactive UI elements, prefer
  locale-safe formatting and semantic HTML over hardcoded string concatenation.


  - Localize every phrase and avoid English-centric word order/spacing.'
repository: cline/cline#v1
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70862
---

When composing user-facing text and interactive UI elements, prefer locale-safe formatting and semantic HTML over hardcoded string concatenation.

- Localize every phrase and avoid English-centric word order/spacing.
  - Build summaries from self-contained, localized verb phrases (e.g., “3 files read”, “2 searches performed”) and then join them using locale-aware list formatting (e.g., Intl.ListFormat) instead of manual `", "`/hardcoded commas.
  - Ensure fallback text is localized when there’s no content to summarize.

- Use native interactive elements for accessibility.
  - If the element is clickable and should respond to keyboard activation (Enter/Space), use `<button type="button">` rather than an `<a>` with click handlers.
  - Keep tests aligned with semantics (assert it’s a real button).

Example pattern (summary building):
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t('chatView:toolGroup.files', { count: counts.read }));
if (counts.list > 0) parts.push(t('chatView:toolGroup.folders', { count: counts.list }));
if (counts.search > 0) parts.push(t('chatView:toolGroup.performedSearches', { count: counts.search }));

if (parts.length === 0) return t('chatView:toolGroup.contextFallback');
const items = new Intl.ListFormat(undefined, { style: 'long', type: 'conjunction' }).format(parts);
return t('chatView:toolGroup.prefixWithItems', { items });
```

Apply these consistently to improve readability and prevent “word salad” outputs across languages, while also ensuring keyboard and assistive-tech friendly behavior for UI controls.