---
title: Locale-Safe Responsive UI
description: 'When writing UI code, treat both layout and user-facing strings as part
  of the “style” contract:


  - **Keep controls reachable under variable content/window sizes**: prefer utility/CSS
  patterns that prevent overflow from cutting interactive regions (e.g., use truncation/shrinking
  instead of a clipping strip for tab labels; cap dialog height and allow...'
repository: Cline/Cline
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70840
---

When writing UI code, treat both layout and user-facing strings as part of the “style” contract:

- **Keep controls reachable under variable content/window sizes**: prefer utility/CSS patterns that prevent overflow from cutting interactive regions (e.g., use truncation/shrinking instead of a clipping strip for tab labels; cap dialog height and allow scrolling in short viewports).
- **Avoid hardcoded grammar/punctuation in localized summaries**: build each segment as a self-contained phrase (verb+noun) and join segments using locale-aware formatting utilities (e.g., Intl.ListFormat). Provide an explicit fallback when there’s nothing to summarize.
- **Document key layout invariants**: if a class/layout choice exists to preserve a visual/interaction guarantee (like an “attached” tab look or preventing clipping), add a short comment so later refactors don’t regress it.

Example pattern for i18n-safe composition:
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
if (counts.list > 0) parts.push(t("chatView:toolGroup.folders", { count: counts.list }));
// ...
if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

const items = new Intl.ListFormat(currentLocale, { style: "long", type: "conjunction" }).format(parts);
return t("chatView:toolGroup.context", { items });
```

This standard prevents “word salad” translations, keeps UI actions clickable, and reduces accidental regressions from future styling changes.