---
title: Locale and semantic UI
description: 'Adopt UI composition rules that keep both text and interactions correct,
  readable, and accessible.


  1) Localize and compose strings safely

  - Avoid hardcoded concatenation/punctuation (e.g., manual `", "` joins, ad-hoc prefixes/suffixes).'
repository: ClInE/cLiNe
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70838
---

Adopt UI composition rules that keep both text and interactions correct, readable, and accessible.

1) Localize and compose strings safely
- Avoid hardcoded concatenation/punctuation (e.g., manual `", "` joins, ad-hoc prefixes/suffixes).
- Make each part a self-contained phrase, then join using locale-aware formatting (e.g., `Intl.ListFormat`) and i18n keys.

Example pattern:
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t('chatView:toolGroup.files', { count: counts.read }));
if (counts.list > 0) parts.push(t('chatView:toolGroup.folders', { count: counts.list }));
if (counts.search > 0) parts.push(t('chatView:toolGroup.performedSearches', { count: counts.search }));

if (parts.length === 0) return t('chatView:toolGroup.contextFallback');
return t('chatView:toolGroup.summary', { items: new Intl.ListFormat(locale).format(parts) });
```

2) Use semantic elements for actions
- If an element triggers behavior (click handler) rather than navigation, prefer a real `<button type="button">` (even if styled like a link).
- This ensures keyboard activation (Enter/Space) and aligns tests with the semantic element.

Example:
```tsx
<button
  type="button"
  className="underline cursor-pointer"
  data-testid="images-unsupported-choose-model"
  onClick={handleModelButtonClick}
>
  {t('chooseModel')}
</button>
```