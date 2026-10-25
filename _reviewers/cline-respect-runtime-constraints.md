---
title: Respect runtime constraints
description: When UI behavior depends on the user’s environment, resolve it at runtime
  with safe defaults (clamping) and preference-aware behavior to prevent jank, layout
  collapse, and unnecessary animation work.
repository: cline/CLINE
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 70839
---

When UI behavior depends on the user’s environment, resolve it at runtime with safe defaults (clamping) and preference-aware behavior to prevent jank, layout collapse, and unnecessary animation work.

Apply this standard:
1) Clamp stored/restored layout dimensions to the current viewport
- If you persist panel heights/positions, clamp on load using window innerHeight (and/or a max-percentage) so window resizes can’t drive content to zero.
- If rendering depends on measuring (e.g., terminal/webview dimensions), re-fit on resize using a ResizeObserver (or equivalent) rather than waiting for user interaction.

2) Honor prefers-reduced-motion for animated/scroll behaviors
- Default to reduced-motion behavior (e.g., “auto”/instant) when prefers-reduced-motion: reduce is set.
- Keep an explicit component prop as an override, but ensure the default path respects the user preference.
- Add tests covering both reduced-motion and non-reduced-motion cases.

Example (motion-aware scroll button):
```ts
function resolveScrollBehavior({ behavior }: { behavior?: 'auto'|'smooth'|'instant' }) {
  const prefersReduced = typeof window !== 'undefined' &&
    window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches;

  if (behavior) return behavior; // explicit prop wins
  return prefersReduced ? 'auto' : 'smooth';
}
```

This approach directly targets performance optimization by preventing unstable layouts on resize and avoiding unnecessary smooth scrolling/animations that can cause perceived jank and wasted work.