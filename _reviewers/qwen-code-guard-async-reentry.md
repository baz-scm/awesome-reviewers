---
title: Guard Async Reentry
description: 'Any UI/logic that performs async work must be resilient to rapid user
  actions and intermediate async states: prevent re-entry, ensure callbacks use the
  latest intended state, and avoid losing results/errors when components unmount.'
repository: QwenLM/qwen-code
label: Concurrency
language: TSX
comments_count: 4
repository_stars: 26407
---

Any UI/logic that performs async work must be resilient to rapid user actions and intermediate async states: prevent re-entry, ensure callbacks use the latest intended state, and avoid losing results/errors when components unmount.

Apply these rules:
1) Guard against re-entry in async handlers
- In submit/click handlers, add an early return when an operation is already in progress (not just `disabled`, since Enter/keyboard can bypass button disabling before re-render).

```ts
const submit = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  if (saving || reloading) return; // prevent duplicate onEnter/rapid submit
  setSaving(true);
  try {
    await onSave(/*...*/);
  } finally {
    setSaving(false);
  }
};
```

2) Prevent concurrent requests
- If there’s a “Reload”/“Delete”/similar action, disable and/or show a spinner during the in-flight promise so repeated clicks can’t overlap.

3) Make timing/streaming callbacks use “latest” state, and verify with tests
- When throttling or scheduling work (setTimeout/rAF), ensure the flush uses the latest value (via ref/state pattern) and add a regression test that triggers multiple updates within one throttle window using fake timers.

4) Be lifecycle-safe for in-flight operations
- Don’t unconditionally dismiss/unmount dialogs while a save is pending.
- If dismissal is allowed, guard state updates (e.g., abort/cancel in-flight work, or ignore late results when closed/unmounted).

5) Handle “connecting/pending” phases deterministically
- If an action can be reversed before a socket/mic/permission finishes, treat it as a pending intent and execute the correct final sequence once the async prerequisite is ready; clear pending intents on actual cancel/cleanup.

This standard targets the real failure modes described: stale/incorrect final results from scheduled callbacks, duplicated async calls (and conflicting revisions), lost errors due to unmount during pending work, and dropped actions when release happens before the underlying connection is ready.