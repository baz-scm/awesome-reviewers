---
title: Locale and accessible UI
description: 'Adopt a UI composition style that’s both accessible and i18n-correct:


  - **Never hardcode concatenation/symbol separators for user-facing summaries** (e.g.,
  avoid `" , "` or ASCII commas for lists). Build **self-contained, locale-ready phrases
  per item** and join them with **`Intl.ListFormat`**.'
repository: cline/cline#v24
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70891
---

Adopt a UI composition style that’s both accessible and i18n-correct:

- **Never hardcode concatenation/symbol separators for user-facing summaries** (e.g., avoid `" , "` or ASCII commas for lists). Build **self-contained, locale-ready phrases per item** and join them with **`Intl.ListFormat`**.
- **Ensure interactive UI controls have proper semantics**: use the correct `role`, expose value ranges with `aria-valuenow/aria-valuemin`, and support keyboard operations (Arrow keys; add modifiers like Shift for step changes where appropriate).
- **Preserve interactive hit targets and visual attachment effects**: prefer **shrink + truncate** (e.g., `min-w-0` + `truncate`) over overflow scrolling when clipping would break the intended joined appearance.

Example (i18n list composition):
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
if (counts.list > 0) parts.push(t("chatView:toolGroup.folders", { count: counts.list }));
if (counts.def > 0) parts.push(t("chatView:toolGroup.definitions", { count: counts.def }));

if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

const list = new Intl.ListFormat(undefined, { style: "long", type: "conjunction" });
const items = list.format(parts);
return t("chatView:toolGroup.prefixWithItems", { items });
```

Example (accessible resize handle pattern):
- Use `role="separator"`, make it focusable (e.g., `tabIndex={0}`), add `aria-valuenow`/`aria-valuemin`, and implement `ArrowUp/ArrowDown` handlers (Shift for larger steps).