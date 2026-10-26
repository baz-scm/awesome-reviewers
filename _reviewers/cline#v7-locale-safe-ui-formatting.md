---
title: Locale-safe UI formatting
description: When writing UI code (especially summaries and dialogs), avoid hardcoded
  language/formatting and ensure components remain usable in constrained viewports.
repository: cline/cline#v7
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70865
---

When writing UI code (especially summaries and dialogs), avoid hardcoded language/formatting and ensure components remain usable in constrained viewports.

**String rules (i18n + locale):**
- Don’t concatenate user-facing sentences from hardcoded English fragments or manual separators (e.g., `", "`).
- Use i18n message keys for each semantic part and keep each part as a self-contained phrase that can be translated.
- Join multiple parts with locale-aware formatting (e.g., `Intl.ListFormat`).
- Provide a clear fallback when there’s no data.

Example pattern:
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t('chatView:toolGroup.files', { count: counts.read }));
if (counts.list > 0) parts.push(t('chatView:toolGroup.folders', { count: counts.list }));
if (counts.def > 0) parts.push(t('chatView:toolGroup.definitions', { count: counts.def }));
if (counts.search > 0) parts.push(t('chatView:toolGroup.performedSearches', { count: counts.search }));

if (parts.length === 0) return t('chatView:toolGroup.contextFallback');

const items = new Intl.ListFormat(locale, { style: 'long', type: 'conjunction' })
  .format(parts);
return items;
```

**Layout rules (responsive/usability):**
- For dialogs/overlays, cap height to the viewport and enable scrolling so actions are reachable on short screens (e.g., `max-h-[calc(100dvh-2rem)]` + `overflow-auto`).
- Prefer accessibility-safe class tweaks that don’t hide focus unintentionally (use `outline-none` only when you have an accessible replacement focus style).