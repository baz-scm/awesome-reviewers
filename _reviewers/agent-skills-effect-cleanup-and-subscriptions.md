---
title: Effect cleanup and subscriptions
description: When using React hooks that interact with external systems (browser events,
  subscriptions, async requests), write code so it cannot leak resources or update
  state after the component unmounts.
repository: vercel-labs/agent-skills
label: React
language: Markdown
comments_count: 2
repository_stars: 26385
---

When using React hooks that interact with external systems (browser events, subscriptions, async requests), write code so it cannot leak resources or update state after the component unmounts.

**Standard**
1. In `useEffect`, always return a cleanup function that removes listeners/subscriptions.
2. For in-flight async work started in `useEffect` (fetch, timers, requests), cancel/abort on cleanup (e.g., `AbortController`) so `setState` can’t run after unmount.
3. For event-based external data that multiple renders/components may depend on, prefer `useSyncExternalStore` over manual event subscription logic.

**Example (safe effect + abort)**
```tsx
function Notifications() {
  const [data, setData] = useState<Notification[]>([])

  useEffect(() => {
    const controller = new AbortController()

    const onResize = () => {
      // listener logic
    }
    window.addEventListener('resize', onResize)

    fetch('/api/notifications', { signal: controller.signal })
      .then(r => r.json())
      .then(next => setData(next))
      .catch(() => {
        /* ignore abort */
      })

    return () => {
      window.removeEventListener('resize', onResize)
      controller.abort()
    }
  }, [])

  return <div />
}
```

**Example (subscription preference)**
- If you’re maintaining state from a browser event source (e.g., `resize`) via listeners, consider modeling that external value with `useSyncExternalStore` rather than ad-hoc `addEventListener` + `setState` patterns.