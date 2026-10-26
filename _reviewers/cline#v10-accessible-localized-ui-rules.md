---
title: Accessible, Localized UI Rules
description: 'Adopt a single UI coding standard for interactive, user-facing components:


  1) Use semantic + ARIA for interactive controls

  - Prefer correct roles (e.g., resize “handle” => `role="separator"`).'
repository: cline/cline#v10
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70869
---

Adopt a single UI coding standard for interactive, user-facing components:

1) Use semantic + ARIA for interactive controls
- Prefer correct roles (e.g., resize “handle” => `role="separator"`).
- Provide required `aria-*` values (e.g., `aria-valuenow`, `aria-valuemin`, `aria-valuemax`).
- Ensure the element is focusable and supports keyboard resizing (e.g., ArrowUp/ArrowDown; optional Shift for larger steps).

2) Make user-facing summaries fully localized
- Do not hardcode punctuation (like `", "`) or assume word order.
- Build each part as a self-contained localized verb phrase.
- Join multiple items using `Intl.ListFormat` for the user’s locale.

3) Keep dialogs/actions reachable on small viewports
- Cap dialog height to the viewport and enable scrolling when needed (e.g., `max-h-[calc(100dvh-...)]` + scroll styles).

Example patterns:

```ts
// 1) Accessible resize handle (pattern)
<div
  role="separator"
  tabIndex={0}
  aria-valuemin={0}
  aria-valuemax={1000}
  aria-valuenow={height}
  onKeyDown={(e) => {
    if (e.key !== "ArrowUp" && e.key !== "ArrowDown") return;
    const step = e.shiftKey ? 48 : 12;
    const delta = e.key === "ArrowUp" ? -step : step;
    onHeightChange(clampTerminalPanelHeight(height + delta, window.innerHeight));
  }}
/>

// 2) Locale-safe list summary (pattern)
const parts = [
  counts.read ? t("chatView:toolGroup.files", { count: counts.read }) : null,
  counts.list ? t("chatView:toolGroup.folders", { count: counts.list }) : null,
].filter(Boolean) as string[];

const list = new Intl.ListFormat(locale, { style: "long", type: "conjunction" }).format(parts);
const summary = parts.length ? t("chatView:toolGroup.contextLabel", { items: list }) : t("chatView:toolGroup.contextFallback");

// 3) Responsive dialog sizing (pattern)
<DialogContent className="max-h-[calc(100dvh-2rem)] overflow-y-auto">
  {/* action buttons remain reachable */}
</DialogContent>
```

Apply this standard during UI code reviews to prevent accessibility regressions, i18n “word salad” issues, and unreachable CTAs in constrained layouts.