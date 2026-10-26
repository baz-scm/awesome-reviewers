---
title: Prefer i18n and semantics
description: 'Adopt a consistent UI coding style:


  - **Localize by construction:** Don’t hardcode English-centric punctuation or stitch
  partial sentences together with `" , "` / `", "`. Instead, translate each logical
  segment (using self-contained verb phrases) and join segments with a locale-aware
  mechanism (e.g., `Intl.ListFormat`).'
repository: cline/cline#v2
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70861
---

Adopt a consistent UI coding style:

- **Localize by construction:** Don’t hardcode English-centric punctuation or stitch partial sentences together with `" , "` / `", "`. Instead, translate each logical segment (using self-contained verb phrases) and join segments with a locale-aware mechanism (e.g., `Intl.ListFormat`).
- **Use native interactive elements:** Any clickable action that behaves like a control must be a real `<button type="button">` (not an `<a>` with `role="button"`), so keyboard activation (Enter/Space) and focus behavior come “for free”.
- **Keep UI primitives consistent:** Prefer shared, repo-standard icon/components (or the same lucide import pattern) to make visual/code verification easier.

Example (locale-safe summary):
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
if (counts.list > 0) parts.push(t("chatView:toolGroup.folders", { count: counts.list }));
if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

const items = new Intl.ListFormat(undefined, { style: "long", type: "conjunction" }).format(parts);
return t("chatView:toolGroup.prefix", { items }); // e.g., "Cline {items}"
```

Example (semantic click target):
```tsx
<button
  type="button"
  onClick={handleModelButtonClick}
  className="underline cursor-pointer"
>
  {t("...choose model")}
</button>
```