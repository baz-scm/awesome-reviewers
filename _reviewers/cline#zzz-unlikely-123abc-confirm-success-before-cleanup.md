---
title: Confirm success before cleanup
description: When an operation can fail, do not perform irreversible side effects
  (detaching a session, discarding a draft, clearing state) until you know the operation
  actually succeeded. Sequence the code so cleanup/commit happens strictly after the
  dependent async call resolves successfully, and treat ambiguous or partial failures
  conservatively rather than assuming...
repository: cline/cline#zzz-unlikely-123abc
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 71035
---

When an operation can fail, do not perform irreversible side effects (detaching a session, discarding a draft, clearing state) until you know the operation actually succeeded. Sequence the code so cleanup/commit happens strictly after the dependent async call resolves successfully, and treat ambiguous or partial failures conservatively rather than assuming success.

For example, resuming a local session from a cloud one should only detach the cloud session after the local restore completes, not before:

```ts
const resumeSession = useCallback(async (sessionId: string) => {
  const result = await propsOnResumeSession(sessionId);
  if (result.ok) {
    // Only detach once we know the local resume actually succeeded.
    detachCloudSession();
  }
  return result;
}, [propsOnResumeSession, detachCloudSession]);
```

Similarly, when deciding whether to restore a draft after a failed send, distinguish between "definitely never sent" and "uncertain delivery" — do not blindly restore/overwrite based on a stale saved record if the send may have partially succeeded or the record may be out of date.

For low-stakes, non-critical side effects (e.g., best-effort fire-and-forget actions like opening an external link), it is acceptable to swallow the error with a `.catch(() => {})` so an unhandled rejection doesn't destabilize the UI — but this pattern should be reserved for cases where failure has no meaningful consequence, not used as a substitute for correctly sequencing state-changing operations.</description>
