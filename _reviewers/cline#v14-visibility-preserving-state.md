---
title: Visibility-Preserving State
description: 'When building React components, treat “UI visibility” and “component
  lifecycle” as separate concerns: avoid unmounting stateful interfaces as a way to
  pause them. Instead, keep long-lived UI mounted and switch it to a hidden/visible
  mode, while explicitly modeling who owns state and events (user vs programmatic;
  focused child vs container).'
repository: cline/cline#v14
label: React
language: TSX
comments_count: 4
repository_stars: 70876
---

When building React components, treat “UI visibility” and “component lifecycle” as separate concerns: avoid unmounting stateful interfaces as a way to pause them. Instead, keep long-lived UI mounted and switch it to a hidden/visible mode, while explicitly modeling who owns state and events (user vs programmatic; focused child vs container).

Apply these rules:
1) Prefer mount-once, hide/show for persistent experiences
- If the UI must preserve state (open conversations, selected session, in-progress flows), mount it once and toggle visibility via props (e.g., <Activity mode="hidden" />) rather than conditional rendering that unmounts effects.
- Ensure hidden mode releases focus traps and pointer-event capture that can block the user during transitions.

2) Make state ownership explicit for event-driven logic
- Separate “user-driven” from “programmatic” actions (e.g., scrollToBottom) so programmatic events don’t incorrectly un-pin/override user intent.
- If the event is async or results in follow-up events, decide exactly when to update state (before the action, on arrival, or only on user input) and encode that in refs/state.

3) Scope keyboard/mouse handlers to the correct event target
- Only react to container-level keyboard shortcuts when the event target is appropriate (e.g., not a focused child control).
- When you intentionally handle a shortcut, stop propagation so other UI (like text inputs) doesn’t receive it unexpectedly.

4) Use refs to keep the latest callbacks in effects
- For callbacks passed into effects/subscriptions, store the latest function in a ref and update it each render; this prevents stale closures without re-subscribing.

Example pattern (visibility toggle + owned state/events):
```tsx
const [mounted, setMounted] = useState(false);
const hubReady = /* derive readiness */;
useEffect(() => { if (hubReady) setMounted(true); }, [hubReady]);

return mounted ? (
  <Activity mode={hubReady ? 'visible' : 'hidden'}>
    <App />
  </Activity>
) : (
  <HubStartupScreen />
);
```
```tsx
// Within an event-driven component: distinguish user vs programmatic
const ourScrollTarget = useRef<number | null>(null);
const pinnedRef = useRef(isPinned);

const scrollToBottom = () => {
  pinnedRef.current = true;
  ourScrollTarget.current = /* clamped target */;
  viewport.scrollTo({ top: viewport.scrollHeight, behavior: 'smooth' });
};

const onScroll = () => {
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (arrived) ourScrollTarget.current = null;
    else return; // treat these events as ours
  }
  // only user-driven scrolling changes pin state
};
```

Adopting this standard reduces bugs from unmount-driven cleanup, prevents hidden UI from trapping focus/pointer interactions during transitions, and makes complex event logic (scroll/keyboard) predictable and testable.