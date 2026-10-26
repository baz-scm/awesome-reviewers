---
title: Locale-aware UI composition
description: 'When implementing user-facing summaries and interactive UI, follow two
  style rules:


  1) Compose translated text from self-contained, grammatical fragments and use locale-aware
  joining.'
repository: cline/cline#v25
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70891
---

When implementing user-facing summaries and interactive UI, follow two style rules:

1) Compose translated text from self-contained, grammatical fragments and use locale-aware joining.
- Avoid hardcoded English punctuation/templates (e.g., manual `", "` joining) inside translatable strings.
- Build each summary “part” independently, then join using a locale formatter (e.g., `Intl.ListFormat`) or translation keys.
- Provide a clear fallback when there is no content to summarize.

Example pattern:
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
if (counts.list > 0) parts.push(t("chatView:toolGroup.folders", { count: counts.list }));
if (counts.def > 0) parts.push(t("chatView:toolGroup.definitions", { count: counts.def }));
if (counts.search > 0) parts.push(t("chatView:toolGroup.performedSearches", { count: counts.search }));

if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

return t("chatView:toolGroup.clinePrefix", {
  items: new Intl.ListFormat(undefined).format(parts),
});
```

2) Use correct native semantics for interactions.
- If it behaves like a button (triggers an action), use `<button type="button">` (even if styled like a link).
- Don’t use `<a>` unless you truly navigate; this prevents keyboard/activation bugs.
- Update tests to assert the semantic element (e.g., “is a button”) so accessibility regressions are caught early.