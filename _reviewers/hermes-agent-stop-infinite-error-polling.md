---
title: Stop Infinite Error Polling
description: In long-running UI workflows that poll (e.g., QR status, task panels,
  gateway actions), treat failures as **transient vs permanent**, and ensure your
  state transitions **cannot loop forever**.
repository: nousresearch/hermes-agent
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 221948
---

In long-running UI workflows that poll (e.g., QR status, task panels, gateway actions), treat failures as **transient vs permanent**, and ensure your state transitions **cannot loop forever**.

Apply this standard:
- **Detect unsupported/permanent capability once** (e.g., 404/“endpoint not available”) → record that state, render an “unavailable”/fallback UI, and **stop the poll** (no repeated `notifyError`).
- **Reset to a terminal/safe state on step failure**: if “apply” (or a critical action) fails, move to an `idle/reset` phase (clearing session IDs, timers, and retry flags) rather than returning to a polling state.
- **Guard polling lifecycle**: use cancellation flags/cleanup so in-flight async calls don’t update state after unmount or after you’ve decided to stop.

Example pattern:
```ts
const [pollingEnabled, setPollingEnabled] = useState(true);
const [phase, setPhase] = useState<'idle'|'waiting'|'applying'>('idle');
const [sessionId, setSessionId] = useState<string|null>(null);

async function fetchStatus() {
  try {
    return await api.getWeixinOnboardingStatus(sessionId!);
  } catch (e: any) {
    // Permanent/unsupported: stop once
    if (e?.status === 404) {
      setPollingEnabled(false);
      setPhase('idle');
      setSessionId(null);
      // show unavailable UI / toast once
      return null;
    }
    throw e; // transient -> let retry logic handle
  }
}

useEffect(() => {
  if (!pollingEnabled || !sessionId || phase !== 'waiting') return;
  let cancelled = false;

  const tick = async () => {
    if (cancelled) return;
    const st = await fetchStatus();
    if (!st) return; // stopped/unavailable
    // ...update UI, schedule next poll...
  };

  const id = setTimeout(() => void tick(), 1500);
  return () => {
    cancelled = true;
    clearTimeout(id);
  };
}, [pollingEnabled, phase, sessionId]);

async function apply() {
  setPhase('applying');
  try {
    await api.applyWeixinOnboarding(sessionId!, {});
    // success path...
  } catch {
    // Critical failure: reset to break retry loop
    setPhase('idle');
    setSessionId(null);
  }
}
```
This prevents repeated error spam and eliminates auto-retry loops when the backend endpoint is unsupported or when a critical step fails.