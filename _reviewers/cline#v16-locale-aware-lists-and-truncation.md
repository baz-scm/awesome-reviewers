---
title: Locale-aware Lists And Truncation
description: 'When formatting user-visible lists (strings) or compact UI strips (tabs/pills),
  avoid hardcoded separators/overflow behavior that breaks readability or usability. '
repository: cline/cline#v16
label: Code Style
language: TSX
comments_count: 2
repository_stars: 70882
---

When formatting user-visible lists (strings) or compact UI strips (tabs/pills), avoid hardcoded separators/overflow behavior that breaks readability or usability. 

Apply two rules:

1) Don’t hardcode punctuation/joins in localized strings
- Prefer building each item as a self-contained phrase, then join with locale-aware formatting (e.g., `Intl.ListFormat`) or use translation strings that handle grammar.
- Example pattern:
```ts
const parts = [
  t("chatView:toolGroup.files", { count: counts.read }),
  t("chatView:toolGroup.folders", { count: counts.list }),
  t("chatView:toolGroup.definitions", { count: counts.def }),
];
if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

const items = new Intl.ListFormat(undefined, { style: "long", type: "conjunction" }).format(parts);
return t("chatView:toolGroup.prefix", { items }); // e.g., "Cline {{items}}"
```

2) Don’t rely on overflow/scrolling that clips important UI affordances
- In flex containers, prefer `min-w-0` + `flex-shrink` and label `truncate`/ellipsis so tabs reduce width instead of overflowing.
- Keep overlay/attached visual effects intact by avoiding overflow clipping from scroll wrappers.
- Example pattern:
```tsx
<div className="flex min-w-0 items-end gap-0.5">
  <div className="min-w-0 truncate">{label}</div>
</div>
```

Result: localized summaries read naturally across languages, and compact UI elements remain usable (controls remain clickable, attached/overlay visuals aren’t clipped) even with many items.