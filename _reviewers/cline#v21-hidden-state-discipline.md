---
title: Hidden State Discipline
description: 'When React UI must survive connectivity, retries, or visibility changes,
  treat lifecycle transitions as first-class:


  - **Preserve state with hide, not unmount (when appropriate):** keep the component
  mounted if you need conversation/session continuity, but ensure hidden mode tears
  down side effects that can harm UX (focus traps, pointer-events, portaled...'
repository: cline/cline#v21
label: React
language: TSX
comments_count: 4
repository_stars: 70886
---

When React UI must survive connectivity, retries, or visibility changes, treat lifecycle transitions as first-class:

- **Preserve state with hide, not unmount (when appropriate):** keep the component mounted if you need conversation/session continuity, but ensure hidden mode tears down side effects that can harm UX (focus traps, pointer-events, portaled dialogs, active recording/listening).
- **Gate one-time bootstrap logic:** if a reconnect/visibility change can re-run effects, ensure navigation/selection “bootstrap” runs **only after the first successful initialization** (use a `ref`/state flag), while still allowing data refresh on later reconnects.
- **Distinguish user intent from programmatic updates:** for event-driven UI (e.g., scroll, recording controls), track whether a change originated from the user vs an internal/programmatic action; only user input should “unpin/disable/cancel,” while programmatic changes should not trigger the same reactions.
- **Keep context scoped to stable boundaries:** don’t synchronize identity-derived/derived links through shared context if the consuming view can derive them from its own fetched identity; reserve context for stable config and shared invariants.

Example (one-time bootstrap after first successful init):
```ts
function useRemoteEnvironmentBootstrap({ status, dispatch }: {
  status: 'starting'|'ready'|'failed';
  dispatch: (action: any) => void;
}) {
  const didBootstrapRef = React.useRef(false);

  React.useEffect(() => {
    if (status !== 'ready') return;
    if (didBootstrapRef.current) {
      // allow refreshes, but avoid re-running selection/navigation bootstrap
      return;
    }
    didBootstrapRef.current = true;
    dispatch({ type: 'select-environment-draft', payload: { /* ... */ } });
  }, [status, dispatch]);
}
```

Apply the same discipline whenever hide/show, reconnect, retries, or programmatic UI updates can cause effects or event handlers to rerun: explicitly define what must be preserved, what must be cleaned up, what must run once, and what must respond only to user intent.