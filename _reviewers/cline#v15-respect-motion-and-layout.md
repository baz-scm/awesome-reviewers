---
title: Respect motion and layout
description: 'Optimize interactive UI by (1) honoring user motion preferences and
  (2) choosing layout strategies that avoid clipping/overflow artifacts.


  1) Motion/scroll performance'
repository: cline/cline#v15
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 70877
---

Optimize interactive UI by (1) honoring user motion preferences and (2) choosing layout strategies that avoid clipping/overflow artifacts.

1) Motion/scroll performance
- For any scroll-to-bottom / smooth-scroll behavior, default to reduced motion when `prefers-reduced-motion: reduce` is set.
- Let an explicit `behavior` prop override the preference.
- Add tests covering both reduced-motion and non-reduced-motion cases.

2) Layout/paint efficiency
- Avoid overflow/scrolling-strip approaches that clip critical UI continuity (e.g., “attached” joins) or reduce click reachability.
- Prefer shrink-to-fit + truncation (e.g., `min-width: 0` and `truncate`/ellipsis) so the active tab effect remains visually connected without relying on clipped containers.

Example (motion-aware scrolling behavior):
```ts
function resolveScrollBehavior({ behavior }: { behavior?: ScrollBehavior }) {
  const prefersReducedMotion =
    typeof window !== "undefined" &&
    window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

  // Explicit prop wins
  if (behavior) return behavior;

  // Default based on user preference
  return prefersReducedMotion ? "auto" : "smooth";
}
```

Example (layout truncation pattern):
```tsx
<div className="flex min-w-0 items-end gap-0.5">
  <span className="min-w-0 truncate">{label}</span>
</div>
```

Apply this as a checklist when implementing/adjusting message scrollers, terminals, or any UI with animated scrolling and dense tab/label layouts.