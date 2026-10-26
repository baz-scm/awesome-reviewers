---
title: Locale and Layout Conventions
description: 'For any user-visible UI (especially summaries, labels, and interactive
  controls), follow these code-style conventions:


  1) Prefer locale-safe list/join formatting'
repository: cline/cline#v13
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70874
---

For any user-visible UI (especially summaries, labels, and interactive controls), follow these code-style conventions:

1) Prefer locale-safe list/join formatting
- Don’t hardcode separators like `", "` in translated strings.
- Build each item as a self-contained phrase and use `Intl.ListFormat` (or an equivalent i18n utility) to join.
- Provide a clear fallback when there are zero parts.

Example:
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
// ...other parts

if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

const items = new Intl.ListFormat(locale, { style: "long", type: "conjunction" })
  .format(parts);
return t("chatView:toolGroup.context", { items });
```

2) Use truncation-friendly flex layout rules (avoid overflow clipping surprises)
- In flex rows where text must truncate, use `min-w-0` on wrappers and `truncate`/ellipsis on labels.
- If the UI relies on visual adjacency (e.g., “attached” tab effects), prefer shrink+truncate over scroll containers that clip/cover the joined visuals.

Rule of thumb:
- Parent flex item: `min-w-0` (not `min-width: auto`).
- Text node: `min-w-0 truncate`.

3) Standardize UI icon/component usage
- Use a consistent icon import pattern across packages (e.g., prefer the same `lucide-react` named icon component usage with the same sizing props) so it’s easy to verify that the same icon style is used everywhere.

Applying this keeps UI readable across locales, prevents layout regressions from overflow/clipping, and improves consistency/verification of visual elements.