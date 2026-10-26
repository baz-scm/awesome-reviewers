---
title: Locale-safe UI strings
description: 'When writing UI code, prefer formatting and markup patterns that are
  readable, localizable, accessible, and consistent.


  - Compose user-facing summaries from **self-contained, locale-translatable fragments**
  (avoid hardcoded punctuation/ordering). Join fragments with **locale-aware list
  formatting** and provide a **clear fallback** when there are no...'
repository: cline/cline#v14
label: Code Style
language: TSX
comments_count: 4
repository_stars: 70876
---

When writing UI code, prefer formatting and markup patterns that are readable, localizable, accessible, and consistent.

- Compose user-facing summaries from **self-contained, locale-translatable fragments** (avoid hardcoded punctuation/ordering). Join fragments with **locale-aware list formatting** and provide a **clear fallback** when there are no fragments.
- For interactive controls, use **semantic HTML** (e.g., `<button type="button">` for actions). Don’t use styled anchors for actions; update tests to assert the correct element type.
- For dialogs/popovers, ensure actions remain reachable on small screens by applying **viewport-based height constraints** and enabling scrolling.
- Keep UI asset usage consistent and easy to audit (e.g., consistent icon import/component patterns).

Example (localized, locale-aware summary composition):
```ts
const parts: string[] = [];

if (counts.read > 0) parts.push(t('chatView:toolGroup.files', { count: counts.read }));
if (counts.list > 0) parts.push(t('chatView:toolGroup.folders', { count: counts.list }));
if (counts.def > 0) parts.push(t('chatView:toolGroup.definitions', { count: counts.def }));
if (counts.search > 0) parts.push(t('chatView:toolGroup.performedSearches', { count: counts.search }));

if (parts.length === 0) return t('chatView:toolGroup.contextFallback');

const items = new Intl.ListFormat(undefined, { style: 'long', type: 'conjunction' }).format(parts);
return t('chatView:toolGroup.summaryPrefix') + ' ' + items;
```

Example (semantic action control):
```tsx
<button
  type="button"
  onClick={handleModelButtonClick}
  className="underline cursor-pointer"
  data-testid="images-unsupported-choose-model"
>
  Choose a different model
</button>
```