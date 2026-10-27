---
title: Render purity and effect lifecycle
description: 'Keep render functions pure and side-effect free, and use hooks/effects
  deliberately rather than by habit.


  1. Never read or write refs during render. Ref access must happen in event handlers
  or effects, since render can run multiple times or be interrupted. If you need a
  value that was previously computed but may become invalid, cache it in a ref and
  update...'
repository: facebook/react#b19
label: React
language: TSX
comments_count: 4
repository_stars: 251893
---

Keep render functions pure and side-effect free, and use hooks/effects deliberately rather than by habit.

1. Never read or write refs during render. Ref access must happen in event handlers or effects, since render can run multiple times or be interrupted. If you need a value that was previously computed but may become invalid, cache it in a ref and update that ref from an effect or event handler, not inline in the render body.

```tsx
// Bad: reading/writing a ref during render
let formattedOptions = '';
if (appliedOptions) {
  formattedOptions = prettyFormat(appliedOptions);
  lastValidOptionsRef.current = formattedOptions; // unsafe during render
} else {
  formattedOptions = lastValidOptionsRef.current;
}

// Good: update the ref from an effect, read it safely elsewhere
useEffect(() => {
  if (appliedOptions) {
    lastValidOptionsRef.current = prettyFormat(appliedOptions);
  }
}, [appliedOptions]);
```

2. Only add a cleanup function to `useEffect` when the effect creates a resource that can leak or whose continued execution after unmount would cause a bug (e.g., `setInterval`, subscriptions, listeners). A single `setTimeout` that naturally expires and has no observable side effect after unmount usually doesn't need cleanup—evaluate case by case instead of adding cleanup reflexively.

3. Prefer existing React primitives over hand-rolled solutions. Before adding manual debouncing with `setTimeout`/refs, check whether `useDeferredValue`, `useTransition`, or similar built-ins already solve the problem; only fall back to manual timers when the built-in behavior is insufficient, and document why.

4. Avoid wasted render work. When a computation (e.g., `useMemo`) only exists to filter or discard most of its output, restructure the logic so the expensive work is skipped entirely for discarded items rather than computed and filtered afterward. Push conditional checks as early as possible in the data pipeline instead of memoizing post-hoc.</description>
</RawReviewerOutputSchema>

