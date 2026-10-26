---
title: Accessible locale-aware UI
description: 'When writing UI code, treat “style” as user-facing correctness: build
  strings for all locales, use semantic interactive elements, and choose layout utilities
  that preserve usability.'
repository: cline/cline#v20
label: Code Style
language: TSX
comments_count: 4
repository_stars: 70886
---

When writing UI code, treat “style” as user-facing correctness: build strings for all locales, use semantic interactive elements, and choose layout utilities that preserve usability.

**1) Compose UI text with locale-safe list joining**
- Avoid hardcoded separators (e.g., `", "`, manual plural logic embedded in mixed phrases).
- Make each item a self-contained verb phrase and join using `Intl.ListFormat` (or equivalent i18n utilities).
- Provide a deterministic fallback when there are no parts.

```ts
function toolGroupSummary(t, counts) {
  const parts: string[] = [];
  if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
  if (counts.list > 0) parts.push(t("chatView:toolGroup.folders", { count: counts.list }));
  if (counts.def > 0) parts.push(t("chatView:toolGroup.definitions", { count: counts.def }));
  if (counts.search > 0) parts.push(t("chatView:toolGroup.performedSearches", { count: counts.search }));

  if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

  const items = new Intl.ListFormat(undefined, { style: "long", type: "conjunction" }).format(parts);
  return t("chatView:toolGroup.summaryPrefix", { items });
}
```

**2) Use semantic elements for interactions**
- For click actions, prefer `<button type="button">` over anchors with `onClick`.
- Ensure tests assert the element type (button) so keyboard activation works by default.

```tsx
<button
  type="button"
  className="underline cursor-pointer"
  onClick={handleModelButtonClick}
>
  Choose a model
</button>
```

**3) Pick layout/styling utilities that avoid clipped interaction**
- Prefer truncation (`min-w-0`, `truncate`) over overflow/clipping that breaks adjacent visual effects.
- For dialogs/panels, cap by viewport height and allow internal scrolling so key actions remain reachable on small screens (e.g., `max-h: calc(100dvh - ...)` + `overflow-y: auto`).

**4) Validate edge cases**
- Test with “worst-case” inputs (many tabs, short viewport heights) to confirm labels remain clickable and critical UI affordances stay accessible.