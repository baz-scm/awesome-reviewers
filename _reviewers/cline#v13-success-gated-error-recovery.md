---
title: Success-Gated Error Recovery
description: 'When an async operation can fail or be retried, make every error/recovery
  path explicit: (1) gate destructive transitions (detach, clear, close, replace restored
  content) on confirmed success, (2) keep user state/invariants intact on failure,
  and (3) when delivery is uncertain, avoid “automatic” restoration and instead restore
  only with evidence (or...'
repository: cline/cline#v13
label: Error Handling
language: TSX
comments_count: 6
repository_stars: 70874
---

When an async operation can fail or be retried, make every error/recovery path explicit: (1) gate destructive transitions (detach, clear, close, replace restored content) on confirmed success, (2) keep user state/invariants intact on failure, and (3) when delivery is uncertain, avoid “automatic” restoration and instead restore only with evidence (or suppress restoration).

Practical rules:
- Delay irreversible side-effects until the success condition is met. Example pattern (detach only after local restore succeeds):
  ```ts
  const resume = async (sessionId: string) => {
    // Don’t detach remote state until local restore is confirmed.
    // detachCloudSession(); // ❌ too early
    const result = await onResumeSession(sessionId);
    if (result.ok) detachCloudSession();
    return result;
  };
  ```
- Don’t clear or overwrite user input until the async action succeeds. If a commit/send fails, preserve the message/draft and allow retry.
- For UI/resource cleanup and failure gating, ensure teardown occurs even when expected events don’t fire (e.g., pointer release outside window) and that startup/failure modes release focus traps/pointer-events deterministically (often by replacing—not covering—the subtree that may contain dialogs).
- For ambiguous delivery outcomes (e.g., “might have dispatched, might not”), suppress restoration of drafts unless you can positively determine “undispatched.” Add end-to-end tests for fail-then-reopen/retry flows.

Testing guidance:
- For every critical failure path, add a test that simulates failure, then validates state after recovery (reconnect/resume/reopen) and verifies that (a) user input wasn’t lost and (b) remote/session resources aren’t left in an inconsistent state.