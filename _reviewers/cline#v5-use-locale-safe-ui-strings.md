---
title: Use locale-safe UI strings
description: 'When building UI summaries/labels from multiple parts, don’t compose
  translated text with hardcoded separators/punctuation.


  **Standard**

  1. Make each “part” a self-contained, translatable phrase (e.g., “{count} files
  read”), not fragments that depend on a fixed English sentence structure.'
repository: cline/cline#v5
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70864
---

When building UI summaries/labels from multiple parts, don’t compose translated text with hardcoded separators/punctuation.

**Standard**
1. Make each “part” a self-contained, translatable phrase (e.g., “{count} files read”), not fragments that depend on a fixed English sentence structure.
2. Join multiple items using a **locale-aware** mechanism (e.g., `Intl.ListFormat`) rather than hardcoding `", "`, `and`, commas, or fixed ordering.
3. If labels may overflow (especially after translation), ensure the layout won’t clip or hide controls: use truncation-safe patterns like `min-w-0` + `truncate` instead of overflow clipping.
4. Use consistent icon/component imports across packages so UI auditability stays high.

**Example (locale-aware joining)**
```ts
import { useMemo } from "react";

function formatToolSummary(t: (k: string, v?: any) => string, counts: any) {
  const parts: string[] = [];

  if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
  if (counts.list > 0) parts.push(t("chatView:toolGroup.folders", { count: counts.list }));
  if (counts.def > 0) parts.push(t("chatView:toolGroup.definitions", { count: counts.def }));
  if (counts.search > 0) parts.push(t("chatView:toolGroup.performedSearches", { count: counts.search }));

  if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

  const items = new Intl.ListFormat(undefined, { style: "long", type: "conjunction" })
    .format(parts);

  return t("chatView:toolGroup.clinePrefix", { items }); // e.g., “Cline {items}”
}
```

**UI overflow safety**
- For tab/label wrappers: prefer `min-w-0` + truncation so localized labels don’t clip interactive affordances.