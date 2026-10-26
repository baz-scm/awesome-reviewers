---
title: Synchronous Claims And Serialization
description: 'Treat concurrency bugs as shared-state coordination problems: prevent
  late or overlapping async work from overwriting/corrupting state, and ensure waits
  are bounded and cancellations clean.'
repository: cline/cline#v18
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 70884
---

Treat concurrency bugs as shared-state coordination problems: prevent late or overlapping async work from overwriting/corrupting state, and ensure waits are bounded and cancellations clean.

Apply these rules:
1) Serialize or coalesce by key
- For any “read-modify-write”, status transition, or stateful side effect, define a coordination key (e.g., sessionId, recordId) and chain operations so only one update for that key runs at a time.
- Also join/queue scheduled refreshes behind in-flight reads rather than letting older results land last.

2) Claim ownership before awaiting
- If multiple submissions/requests can target the same pending action, claim it synchronously (set a “handled” marker / clear the pending resolver) before any `await` that prepares attachments or performs network IO.
- Route subsequent submissions to a different path (e.g., follow-up) once the claim is taken.

Example (claim before await):
```ts
async function resolvePendingAskQuestion(options: {
  prompt?: string;
  images?: string[];
  files?: string[];
  deliverAttachments?: (isCurrent: () => boolean) => Promise<void>;
}) {
  const resolve = pendingAskResolve;
  if (!resolve) return false;

  // Claim synchronously: after this line, nobody else can resolve this same question.
  pendingAskResolve = undefined;

  const hasAttachments = (options.images?.length ?? 0) > 0 || (options.files?.length ?? 0) > 0;
  const responseText = options.prompt ?? "";

  let echoLocally = Boolean(responseText);
  if (hasAttachments && options.deliverAttachments) {
    try {
      // Optionally guard delivery continuation against cancellation/replacement.
      await options.deliverAttachments(() => true);
      echoLocally = false;
    } catch {
      // Fail open: deliver text rather than leaving the run suspended.
    }
  }

  if (echoLocally) appendUserFeedback(responseText);
  setTurnPhase("streaming");
  resolve(responseText);
  return true;
}
```

3) Bound potentially unending waits
- Any await that can be blocked by another party going away (disconnection/unregister) must have a deadline policy.
- If some waits depend on human approval, treat those as a separate timeout/cancellation policy.

4) Make cancellation real and cleanup complete
- Pass abort signals through to sleeps, fetch/streams, and retry loops; don’t just check `cancelled()` after work completes.
- On promise settlement (especially when using “exit” vs “close” fallbacks), unregister listeners and dispose timers/pipes so late completions can’t leak resources or keep processes alive.

5) When deferring, capture the exact target immediately
- If you schedule work to run later, capture the specific identifier/handle/index needed to apply the result (don’t re-search for “latest” later, which causes out-of-order corruption).

This standard prevents the specific concurrency failures seen across teardown status overwrites, overlapping deliveries, forever-hangs, out-of-order checkpoint/state updates, and subprocess/listener leaks.