---
title: Concurrency Safety Contracts
description: 'When multiple async operations can overlap (user submits twice, retries/timeouts,
  reconnects, background work), enforce a single ownership/ordering contract:'
repository: cline/cline#v22
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 70886
---

When multiple async operations can overlap (user submits twice, retries/timeouts, reconnects, background work), enforce a single ownership/ordering contract:

1) Claim state synchronously before any await
- For any “pending resolver” (pending question, pending reply, pending session attachment), set/clear the resolver/ownership immediately, then await delivery/prep.
- This prevents a second overlapping call from resolving the same pending item or stealing delivery.

2) Correlate every async continuation with an ownership token
- Use a generation/attempt id (or captured handle) captured at the start of the async operation.
- After each await, check the token; if it doesn’t match current ownership, exit without applying results.

3) Capture update targets before starting background work
- If you will update a specific UI/state entity after an async task completes, capture the exact reference/identifier/index synchronously.
- Don’t “find the last matching thing” later.

4) Make timeouts/aborts clean up late completions
- If you abort because a deadline passed, ensure any later resolve/reconnect still performs required cleanup (e.g., disconnect/close, remove listeners/pipes, cancel pumps).

Example (claim-before-await + token gating)
```ts
let pending: undefined | ((text: string) => void);
let attempt = 0;

async function resolvePendingAskQuestion(params: {
  text?: string;
  images?: string[];
  files?: string[];
  deliverAttachments?: () => Promise<void>;
}) {
  if (!pending) return false;

  // 1) claim immediately
  const resolve = pending;
  pending = undefined;
  const myAttempt = ++attempt;

  const hasAttachments = Boolean((params.images?.length ?? 0) > 0 || (params.files?.length ?? 0) > 0);

  if (hasAttachments && params.deliverAttachments) {
    // 2) gate late continuations
    await params.deliverAttachments();
    if (myAttempt !== attempt) return true; // ownership moved; do not double-apply
  }

  resolve(params.text ?? "");
  return true;
}
```

Checklist to apply during review
- Does any code call/resolve/serve “pending X” in a way that could be overtaken by a second overlapping submission? (If yes: claim before await.)
- After awaits, does the code verify it still owns/apply-to the same logical entity? (If no: add a token/captured reference.)
- Does background completion re-scan for “latest” state instead of updating a captured target? (If yes: capture before await.)
- When a timeout/abort triggers, is late work guaranteed to release resources (connections, timers, event listeners, pipes)? (If no: add late-cleanup paths.)

Adopting this contract prevents the recurring failure modes seen in the discussions: stolen pending resolutions, stale async callbacks mutating newer state, incorrect late updates due to post-await re-search, and resource leaks from timeouts/aborts that don’t clean up late completions.