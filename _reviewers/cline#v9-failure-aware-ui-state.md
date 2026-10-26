---
title: Failure-aware UI State
description: When failures happen (async rejects, missed lifecycle events, or reconnect/startup
  changes), the UI must remain consistent, preserve user input, clean up correctly,
  and recover automatically.
repository: cline/cline#v9
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70868
---

When failures happen (async rejects, missed lifecycle events, or reconnect/startup changes), the UI must remain consistent, preserve user input, clean up correctly, and recover automatically.

Apply these rules:
- **Gate state transitions on success:** only clear/commit/advance UI state after the async operation actually succeeds; preserve inputs on rejection.
- **Retry recovery on connectivity/lifecycle changes:** if an initialization lookup can fail, re-run it when the transport/state becomes “connected/ready” again (e.g., sidecar reconnect).
- **Use safe failure-mode UI routing:** when a higher-level system enters a failure state, actively **replace/unmount** the prior interactive UI instead of merely covering it—prevents focus/pointer-event traps.
- **Make event-driven interactions resilient:** for drags/resizes, ensure cleanup (listeners/body styles) happens even if the expected terminating event (e.g., `pointerup`) is not delivered.

Example (success-gated commit message):
```ts
const commit = useCallback(async () => {
  // don’t clear user input until success
  await onAction({ type: "commit", message: message.trim(), push: true });
  setMessage("");
}, [onAction, message]);
```
Example (recovery on reconnect):
```ts
useEffect(() => {
  if (transport !== "connected") return;
  desktopClient.invoke<string>("get_cline_app_base_url").then(setClineAppBaseUrl);
}, [transport]);
```
Example (failure-mode replacement):
```tsx
{loaded ? <App /> : <HubStartupScreen />}
// and if hub later fails, swap back instead of covering App
```