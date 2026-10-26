---
title: Gate State on Success
description: Update UI state and side effects only after you’ve confirmed the operation
  succeeded; on failure, preserve the prior state/resources and ensure cleanup still
  runs.
repository: cline/cline#v27
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70892
---

Update UI state and side effects only after you’ve confirmed the operation succeeded; on failure, preserve the prior state/resources and ensure cleanup still runs.

Apply these rules:
- Preserve invariants on failure: don’t detach/close/clear anything irreversible until the corresponding restore/commit resolves successfully.
- Implement explicit recovery points: when an async call depends on a connection/sidecar/transport that can reconnect, trigger the lookup/retry from the transport state rather than requiring a separate refresh tied to unrelated state.
- Defend against missing events: for drag/listener patterns, add logic to end/cleanup when an expected event (like pointerup) doesn’t arrive (e.g., release outside window).
- Test failure paths: add tests where the async action rejects/fails and assert that state (messages, attachments, UI) remains correct.

Example pattern (async gated state + failure-safe UI):
```ts
const [message, setMessage] = useState("");

async function commit() {
  const trimmed = message.trim();
  if (!trimmed) return;

  try {
    // Keep current message until success
    const ok = await onAction({ type: "commit", message: trimmed });
    if (!ok) return; // don’t clear on failure
    setMessage("");   // clear only on success
  } catch {
    // leave message intact; optionally show toast/error
  }
}
```

Also ensure recovery/cleanup:
- Retry lookups on reconnect/transport state changes.
- Ensure drag listeners/styles are restored even if the normal termination event doesn’t fire.