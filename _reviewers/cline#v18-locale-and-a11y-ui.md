---
title: Locale and A11y UI
description: 'When implementing UI components, treat user-facing text and interactive
  layout as “part of the code style”:


  - i18n: Don’t hardcode sentence structure or punctuation (e.g., commas/“Cline …”
  concatenation). Build summaries from translation keys and join parts using locale-aware
  formatting (e.g., Intl.ListFormat), with an explicit fallback for empty context.'
repository: cline/cline#v18
label: Code Style
language: TSX
comments_count: 4
repository_stars: 70884
---

When implementing UI components, treat user-facing text and interactive layout as “part of the code style”:

- i18n: Don’t hardcode sentence structure or punctuation (e.g., commas/“Cline …” concatenation). Build summaries from translation keys and join parts using locale-aware formatting (e.g., Intl.ListFormat), with an explicit fallback for empty context.
- Accessibility: Interactive affordances must be keyboard-usable and properly described (role/aria, focusable elements, keyboard handlers like ArrowUp/ArrowDown for slider-like controls).
- Responsive layout: Cap dialog/panel content to the viewport and make it scrollable so secondary actions remain reachable in short windows.
- Overflow/clipping: Avoid overflow/scroll wrappers when they clip critical controls/effects; prefer shrink + truncate for tab labels/strips so essential buttons stay clickable.

Example (locale-safe summary building):

```ts
import { IntlMessageFormat } from "intl-messageformat"; // or your existing t() system

const parts: string[] = [];
if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
if (counts.list > 0) parts.push(t("chatView:toolGroup.folders", { count: counts.list }));
if (counts.def > 0) parts.push(t("chatView:toolGroup.definitions", { count: counts.def }));
if (counts.search > 0) parts.push(t("chatView:toolGroup.performedSearches", { count: counts.search }));

if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

const items = new Intl.ListFormat(undefined, { style: "long", type: "conjunction" }).format(parts);
return t("chatView:toolGroup.summary", { items }); // e.g., "Cline {{items}}"
```

Apply the same mindset to interactive layout: add the needed ARIA/keyboard support and ensure the container uses responsive sizing (max-height + scroll) so all actions stay reachable.