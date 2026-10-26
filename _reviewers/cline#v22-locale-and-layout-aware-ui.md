---
title: Locale and Layout-Aware UI
description: When writing user-visible UI code, avoid hardcoded formatting assumptions
  (text joining/separators or layout overflow strategies). Prefer locale-aware formatting
  for strings and shrink/truncate behavior for responsive UI.
repository: cline/cline#v22
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70886
---

When writing user-visible UI code, avoid hardcoded formatting assumptions (text joining/separators or layout overflow strategies). Prefer locale-aware formatting for strings and shrink/truncate behavior for responsive UI.

Apply this standard:
- Text summaries: compose each item as a self-contained, localized phrase, then join with a locale-aware list formatter (e.g., `Intl.ListFormat` / existing i18n helpers). Provide a clear fallback when there’s no content.
- Responsive controls/tabs: ensure flex items can actually shrink (`min-w-0`) and labels use `truncate` so essential controls remain clickable; avoid overflow/scroll patterns that clip important attached/connected visuals.

Example (localized join pattern):
```ts
const parts = [
  t('chatView:toolGroup.files', { count: counts.read }),
  t('chatView:toolGroup.folders', { count: counts.list }),
].filter(Boolean);

if (parts.length === 0) return t('chatView:toolGroup.contextFallback');

const items = new Intl.ListFormat(currentLocale, {
  style: 'long',
  type: 'conjunction',
}).format(parts);

return t('chatView:toolGroup.summary', { items });
```

Example (tab shrink/truncate pattern):
```tsx
<div className="flex min-w-0 items-end gap-0.5">
  <span className="min-w-0 truncate">{tab.label}</span>
  {/* keep + / hide buttons outside the truncated region */}
</div>
```