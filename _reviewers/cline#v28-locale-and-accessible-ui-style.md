---
title: Locale and Accessible UI Style
description: 'Adopt a “UI-ready code style” that covers layout, accessibility, and
  locale-safe text.


  **Rules**

  1. **Preserve critical UI controls:** When tab/label counts can grow, prefer `min-w-0`
  + `truncate`/ellipsis over scrolling or overflow clipping—so important buttons (e.g.,
  add/close) stay visible and clickable.'
repository: cline/cline#v28
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70893
---

Adopt a “UI-ready code style” that covers layout, accessibility, and locale-safe text.

**Rules**
1. **Preserve critical UI controls:** When tab/label counts can grow, prefer `min-w-0` + `truncate`/ellipsis over scrolling or overflow clipping—so important buttons (e.g., add/close) stay visible and clickable.
2. **Use semantic roles + ARIA for interactive affordances:** For adjustable/resize handles, use `role="separator"` and appropriate `aria-valuemin/aria-valuemax/aria-valuenow`; ensure the element is focusable and supports keyboard resizing (ArrowUp/ArrowDown; Shift for larger steps).
3. **Build locale-safe summaries:** Don’t hardcode punctuation/word order by concatenating strings (e.g., English-style `"Cline {{items}}"` with `", "`). Instead:
   - Make each translated “part” a self-contained verb phrase (so other languages can reorder safely).
   - Join parts with `Intl.ListFormat` for the user’s locale.

**Example (locale-safe join with verb-phrase parts)**
```ts
const parts: string[] = [];
if (counts.read > 0) {
  parts.push(t("chatView:toolGroup.files", { count: counts.read }));
}
if (counts.search > 0) {
  parts.push(t("chatView:toolGroup.performedSearches", { count: counts.search }));
}

if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

const items = new Intl.ListFormat(locale, { type: "conjunction" }).format(parts);
return t("chatView:toolGroup.summary", { items }); // translation controls final word order
```

**Checklist for PRs**
- UI: At max expected item counts, are all key controls still reachable (no clipped join/overflows)?
- Accessibility: Do interactive handles have correct role/ARIA and keyboard support?
- i18n: Are user-facing summaries built from translated, self-contained phrases and joined via `Intl.ListFormat` (no hardcoded commas/punctuation)?