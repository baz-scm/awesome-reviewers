---
title: Preserve state, control scroll
description: 'When React UI depends on async readiness or complex user interaction,
  avoid brittle inference and make intent explicit:


  1) Prefer hiding over unmounting for stateful trees'
repository: cline/cline#v12
label: React
language: TSX
comments_count: 4
repository_stars: 70872
---

When React UI depends on async readiness or complex user interaction, avoid brittle inference and make intent explicit:

1) Prefer hiding over unmounting for stateful trees
- If the UI should “come back where it left off” after retries/recovery, keep it mounted and hide it while showing a startup/overlay state.
- Only unmount/replace when you need to prevent duplicated controls, fix focus/portal trapping, or reset failure-specific UI.

2) Use explicit props/signals for intent vs derived guesses
- Don’t infer “send”, “hydration”, or “session switching” from indirect counters; pass explicit booleans/flags from the source of truth.
- For UI state like scroll pinning, accept an `initial*` prop and apply it only on first mount (later prop changes must not silently override user control).

3) Distinguish user intent from programmatic updates
- For scroll/auto-scroll behavior: track programmatic targets in a ref and ignore scroll events that are the result of your own commands.
- Un-pin/pin based on user input (wheel/keyboard) rather than the downstream async scroll event.
- Gate key handlers so focused child controls don’t trigger unintended state changes.

Example pattern (scroll + intent separation):
```tsx
function distanceFromBottom(viewport: HTMLDivElement) {
  return viewport.scrollHeight - viewport.scrollTop - viewport.clientHeight;
}

function Conversation({ initialScrollState, onScrollStateChange, ...props }) {
  const [pinned, setPinnedState] = useState(initialScrollState?.pinned ?? true);
  const pinnedRef = useRef(pinned);
  const ourScrollTarget = useRef<number | null>(null);
  const onScrollStateChangeRef = useRef(onScrollStateChange);
  onScrollStateChangeRef.current = onScrollStateChange;

  const setPinned = useCallback((next: boolean) => {
    pinnedRef.current = next;
    setPinnedState(next);
  }, []);

  const writeScrollTop = useCallback((el: HTMLDivElement, top: number) => {
    const maxTop = Math.max(0, el.scrollHeight - el.clientHeight);
    const clamped = Math.min(Math.max(0, top), maxTop);
    ourScrollTarget.current = clamped !== el.scrollTop ? clamped : null;
    el.scrollTo({ top: clamped, behavior: 'smooth' });
  }, []);

  useEffect(() => {
    if (!props.viewportEl) return;
    const viewport = props.viewportEl;

    const handleScroll = () => {
      if (ourScrollTarget.current !== null) {
        const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
        if (arrived || pinnedRef.current) {
          if (arrived) ourScrollTarget.current = null;
          return;
        }
        ourScrollTarget.current = null;
      }

      const dist = distanceFromBottom(viewport);
      const nextPinned = dist <= 20;
      setPinned(nextPinned);
      onScrollStateChangeRef.current?.({
        pinned: nextPinned,
        scrollTop: viewport.scrollTop,
      });
    };

    const handleWheel = (e: WheelEvent) => {
      if (e.deltaY < 0) setPinned(false);
    };

    viewport.addEventListener('scroll', handleScroll);
    viewport.addEventListener('wheel', handleWheel, { passive: true });
    return () => {
      viewport.removeEventListener('scroll', handleScroll);
      viewport.removeEventListener('wheel', handleWheel);
    };
  }, [setPinned, props.viewportEl]);

  return null;
}
```

Adopt this standard to prevent: (a) state loss across async UI transitions, (b) focus/portal trapping from uncoordinated overlay mounting, (c) incorrect behavior from derived/brittle signals, and (d) scroll/input bugs caused by conflating your programmatic actions with the reader’s intent.