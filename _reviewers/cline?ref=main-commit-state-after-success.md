---
title: Commit state after success
description: When an operation can fail, do not mutate shared state, detach dependencies,
  or hide error-adjacent data until you have confirmed the operation actually succeeded.
  Sequencing a destructive or irreversible state change before an async call resolves
  can leave the system in an inconsistent state if that call fails.
repository: cline/cline?ref=main
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 70980
---

When an operation can fail, do not mutate shared state, detach dependencies, or hide error-adjacent data until you have confirmed the operation actually succeeded. Sequencing a destructive or irreversible state change before an async call resolves can leave the system in an inconsistent state if that call fails.

For example, prefer:
```ts
const resumeSession = async (sessionId: string) => {
	const result = await propsOnResumeSession(sessionId);
	// Only detach the cloud session once the local resume has succeeded.
	detachCloudSession();
	return result;
};
```
over detaching before the await, which leaves a failed resume unrecoverable.

The same principle applies to rendering: when an error is present, don't fall back to rendering stale or placeholder "success" data (e.g. a bundled model list) as if nothing went wrong — hide it or show the error instead, so users aren't misled into thinking the operation succeeded (`modelList.length > 0 && !modelsError`).

Similarly, when retrying a failed async lookup, tie the retry to the event that actually governs the dependency (e.g. retry on transport reconnect if the value depends on the sidecar environment) rather than to an unrelated trigger (e.g. account refresh), so recovery happens reliably and at the right time.