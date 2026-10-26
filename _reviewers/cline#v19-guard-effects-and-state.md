---
title: Guard Effects and State
description: 'When React components are hidden/shown or re-rendered due to async/transport
  changes, ensure user state and UI intent are preserved.


  Apply these rules:'
repository: cline/cline#v19
label: React
language: TSX
comments_count: 3
repository_stars: 70885
---

When React components are hidden/shown or re-rendered due to async/transport changes, ensure user state and UI intent are preserved.

Apply these rules:
1) Prefer hide/show over remount for stateful UIs
- If hiding is what you need, keep the primary app mounted and only toggle visibility. This preserves conversation selection and prevents focus-trap/pointer-event regressions caused by tearing down portaled dialogs.

2) Make “initialization/navigation” explicitly one-time (per successful condition)
- If an effect can re-run during visibility toggles (or remount-like behavior), prevent it from re-dispatching actions that should only happen once.
- Pattern: use a ref (not state) as a “first successful load” gate; refresh relevant data on every load, but only run navigation/selection once after success.

3) Separate user input from programmatic updates
- For interaction-driven state (e.g., scroll/pinning), track programmatic targets and ignore/handle their resulting events so they don’t get misclassified as user intent.
- Also gate event handling by event origin (e.g., only treat arrow keys/unpin when the event target is the viewport, not a focused child control).

Example (combines the patterns):
```tsx
function useOneTimeAfterSuccess(run: () => void, ok: boolean) {
  const didRunRef = React.useRef(false);
  React.useEffect(() => {
    if (!ok) return;
    if (didRunRef.current) return;
    didRunRef.current = true;
    run();
  }, [ok, run]);
}

function ConversationViewport({ initialScrollState }: { initialScrollState?: any }) {
  const viewportRef = React.useRef<HTMLDivElement | null>(null);
  const ourScrollTarget = React.useRef<number | null>(null);

  const scrollToBottom = (behavior: ScrollBehavior) => {
    const el = viewportRef.current;
    if (!el) return;
    ourScrollTarget.current = el.scrollHeight;
    el.scrollTo({ top: el.scrollHeight, behavior });
  };

  const onScroll = () => {
    const el = viewportRef.current;
    if (!el) return;
    if (ourScrollTarget.current != null) {
      // Ignore scroll events caused by scrollToBottom.
      if (Math.abs(el.scrollTop - ourScrollTarget.current) <= 1) ourScrollTarget.current = null;
      return;
    }
    // Handle real reader intent here...
  };

  return <div ref={viewportRef} onScroll={onScroll} />;
}
```

Use this standard to prevent accidental focus issues, broken selections, and unintended state changes caused by effect re-execution, remount-like behavior, or misattributed input events.