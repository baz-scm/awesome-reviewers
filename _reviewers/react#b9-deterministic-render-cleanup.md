---
title: Deterministic Render & Cleanup
description: 'Ensure React renders stay deterministic and free of dependency on mutable
  ref state, and that any time-based side effects are properly cleaned up.


  Apply these rules:'
repository: facebook/react#b9
label: React
language: TSX
comments_count: 2
repository_stars: 251891
---

Ensure React renders stay deterministic and free of dependency on mutable ref state, and that any time-based side effects are properly cleaned up.

Apply these rules:
1) Avoid ref reads for correctness inside render
- Don’t use `someRef.current` during the render pass to decide what to display/state to commit.
- If you need “last known good” values, compute/store them outside render (e.g., in your store/dispatch flow) or update component state via effects.

2) Move validation/derivation out of render
- When rendering depends on whether options are valid, validate/format in the state layer.
- If invalid, keep the previous valid value in the store rather than consulting a ref during render.

3) Cleanup timers/effects
- If you create resources with potential to outlive the component (intervals, subscriptions, pending async work), add cleanup in `useEffect`.
- Timeouts can also require cleanup if cancellation matters on unmount.

Example pattern:
```tsx
// Store/dispatch layer decides whether to update
function setOptions(next: unknown) {
  const parsed = validateAndFormat(next);
  if (!parsed.valid) return; // keep previous valid options
  store.update({ appliedOptions: parsed.value });
}

// Component render stays deterministic
function ConfigEditorView({ appliedOptions }: { appliedOptions?: string }) {
  return <pre>{appliedOptions ?? 'Invalid configs'}</pre>;
}

// Timer cleanup
useEffect(() => {
  const id = setTimeout(() => dispatchDebouncedChange(), 500);
  return () => clearTimeout(id);
}, [dispatchDebouncedChange]);
```

This prevents subtle correctness issues tied to mutable refs and reduces memory-leak/late-dispatch problems from timers and other side effects.