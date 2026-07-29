---
title: Hot Path Efficiency
description: 'Default to “do the minimum possible work per hot-path update.”


  Apply these checks:

  1) Early-exit before side effects

  - If a piece of async work is no longer relevant (stale session, unmounted view,
  toggled-away state), return before starting the network call/timer/observer.'
repository: QwenLM/qwen-code
label: Performance Optimization
language: TSX
comments_count: 8
repository_stars: 26407
---

Default to “do the minimum possible work per hot-path update.”

Apply these checks:
1) Early-exit before side effects
- If a piece of async work is no longer relevant (stale session, unmounted view, toggled-away state), return before starting the network call/timer/observer.

2) Keep props/callbacks stable during streaming
- If a child is `React.memo`’d (or any memoized subtree), don’t pass freshly-created inline handlers every render. Use `useCallback` (and `useMemo` for derived values) so shallow prop comparisons remain true.

3) Don’t recreate observers/effects due to irrelevant dependencies
- For `ResizeObserver`/event listeners, only depend on values actually used by the effect. If the effect body doesn’t read a dependency, removing it prevents unnecessary teardown/re-setup during frequent rerenders.

4) Throttle at the right stage + memoize expensive transforms
- When throttling streaming content, throttle the raw rapidly-changing input *before* expensive parsing/transforms so the transform runs no more often than intended.
- Avoid dependency patterns that create self-perpetuating timeout chains; use refs for “latest value” and keep effect deps minimal.
- Even with throttling, memoize the expensive transform so it runs only when the throttled input (or other required inputs) actually change.

5) Detect changes against consistent baselines
- When deciding whether to write settings / trigger refresh, compare the same effective-state lists (not a filtered list vs an unfiltered one) to avoid spurious no-op writes.

Example (stable handler + throttled transform):
```ts
const handleRightPanelOpen = useCallback((request: TurnOutputOpenRequest) => {
  if (request.kind === 'subagent') {
    onRightPanelOpen?.({ /* ... */ });
  }
}, [onRightPanelOpen]);

const throttledContent = useThrottledValue(content ?? '', isStreaming);
const renderedContent = useMemo(() => {
  if (throttledContent && source && sourceMarkdown?.transformMarkdown) {
    return sourceMarkdown.transformMarkdown(throttledContent, { source });
  }
  return throttledContent;
}, [throttledContent, source, sourceMarkdown?.transformMarkdown]);
```

Use this standard to review PRs that touch streaming, parsing, rendering, observers, and settings-change detection.