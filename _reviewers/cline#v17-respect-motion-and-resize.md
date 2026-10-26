---
title: Respect Motion And Resize
description: 'For performance-sensitive UI (scrolling, terminals, animated panels),
  ensure two things: (1) motion defaults honor user accessibility preferences, and
  (2) persisted layout sizes are clamped to the current viewport with targeted re-fit
  when constraints change.'
repository: cline/cline#v17
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 70883
---

For performance-sensitive UI (scrolling, terminals, animated panels), ensure two things: (1) motion defaults honor user accessibility preferences, and (2) persisted layout sizes are clamped to the current viewport with targeted re-fit when constraints change.

- Motion: default animation/scroll behavior should follow `prefers-reduced-motion` (disable/auto when reduced; smooth otherwise). If the caller explicitly sets a `behavior`/mode prop, that override should win.
- Resize/Layout restoration: when restoring persisted panel sizes/heights, clamp them against current viewport dimensions and use `ResizeObserver` (or equivalent) to re-fit heavy components (e.g., terminals) only when the imposed cap becomes active.

Example (motion + clamped resize):
```tsx
import { useEffect, useMemo, useState } from "react";

function prefersReducedMotion() {
  return typeof window !== "undefined" &&
    window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
}

export function ScrollButton({ behavior, onClick }: {
  behavior?: ScrollBehavior;
  onClick?: () => void;
}) {
  const autoBehavior = useMemo(() => (
    prefersReducedMotion() ? "auto" : "smooth"
  ), []);

  const resolvedBehavior = behavior ?? autoBehavior;

  return (
    <button
      onClick={() => {
        onClick?.();
        document.documentElement.scrollTo({ top: 0, behavior: resolvedBehavior });
      }}
    >
      Scroll
    </button>
  );
}

export function useClampedPanelHeight(persistedHeight: number) {
  const [height, setHeight] = useState(() => persistedHeight);

  useEffect(() => {
    const maxH = Math.floor(window.innerHeight * 0.8); // clamp
    setHeight(Math.min(persistedHeight, maxH));

    const ro = new ResizeObserver(() => {
      const cap = Math.floor(window.innerHeight * 0.8);
      setHeight(prev => (prev > cap ? cap : prev));
      // also trigger any expensive component re-fit here (e.g., terminal xterm.fit())
    });
    ro.observe(document.body);
    return () => ro.disconnect();
  }, [persistedHeight]);

  return height;
}
```