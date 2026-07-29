---
title: Consistent UI Formatting
description: 'Apply consistent, presentation-focused code style to UI components:


  - Preserve flex/height semantics on “fill” containers: when a layout depends on
  full-viewport panels, ensure the relevant containers keep the same flex height/overflow
  utilities (e.g., `flex`, `flex-col`, `h-full`, `min-h-0`, and the intended `overflow-*`
  behavior).'
repository: maximhq/bifrost
label: Code Style
language: TSX
comments_count: 3
repository_stars: 6862
---

Apply consistent, presentation-focused code style to UI components:

- Preserve flex/height semantics on “fill” containers: when a layout depends on full-viewport panels, ensure the relevant containers keep the same flex height/overflow utilities (e.g., `flex`, `flex-col`, `h-full`, `min-h-0`, and the intended `overflow-*` behavior).
- Make truncation reliable (especially with tooltips): use the correct element display semantics so truncation actually applies—commonly `className="block truncate ..."` on the text node used by the tooltip trigger.
- Centralize shared formatting: any non-trivial formatting logic (currency/token/number conversions) should live in shared utilities (e.g., `ui/lib/utils/numbers.ts`) rather than being reimplemented in components.
- Separate derived presentation values: in `useMemo`, precompute display strings and tooltip strings separately (e.g., rounded display, full-precision tooltip) instead of mixing formatting logic inline.

Example pattern:
```ts
const statCards = useMemo(() => {
  const display = stats
    ? stats.success_rate.toFixed(2) + "%"
    : undefined;
  const tooltip = stats
    ? stats.success_rate.toLocaleString(undefined, { maximumFractionDigits: 6 })
    : undefined;

  return [{
    title: "Success Rate",
    value: fetchingStats ? <Skeleton /> : display ?? "-",
    tooltip: fetchingStats ? undefined : tooltip,
    testId: "logs-stat-value-success-rate",
  }];
}, [fetchingStats, stats]);
```
This keeps UI layout stable, prevents truncation/tooltip bugs, improves readability, and ensures consistent formatting across the app.