---
title: Locale-Safe UI Style
description: 'Adopt UI composition patterns that keep text translatable, controls
  accessible, and layout reliable.


  1) Build i18n strings from self-contained parts

  - Avoid hardcoded separators/phrases like `", "` or English-specific scaffolding
  (e.g., `" read "`).'
repository: cline/cline#v30
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70894
---

Adopt UI composition patterns that keep text translatable, controls accessible, and layout reliable.

1) Build i18n strings from self-contained parts
- Avoid hardcoded separators/phrases like `", "` or English-specific scaffolding (e.g., `" read "`).
- Create each segment as a complete, localizable phrase, then join them using locale-aware formatting (e.g., `Intl.ListFormat`).
- Ensure your fallback path returns a fully translated string.

Example:
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
if (counts.list > 0) parts.push(t("chatView:toolGroup.folders", { count: counts.list }));
if (counts.def > 0) parts.push(t("chatView:toolGroup.definitions", { count: counts.def }));
if (counts.search > 0) parts.push(t("chatView:toolGroup.performedSearches", { count: counts.search }));

if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

const items = new Intl.ListFormat(locale, { style: "long", type: "conjunction" }).format(parts);
return t("chatView:toolGroup.context", { items }); // e.g., "Cline {{items}}"
```

2) Use native interactive elements
- If the element triggers an action, use the correct semantic element (e.g., `<button type="button">` instead of an `<a>` used like a button).
- Let accessibility behavior (keyboard, role) come from semantics; styling can mimic link appearance.

3) Prefer truncation over clipping/overflow that breaks UI affordances
- For tab strips with many items, use flex sizing + truncation utilities (e.g., `min-w-0` and `truncate`) so labels shrink while important controls remain visible/clickable.
- Avoid overflow modes that clip visually critical “attached” effects.

Applying these rules consistently will reduce locale regressions, improve keyboard accessibility, and prevent layout choices that degrade usability.