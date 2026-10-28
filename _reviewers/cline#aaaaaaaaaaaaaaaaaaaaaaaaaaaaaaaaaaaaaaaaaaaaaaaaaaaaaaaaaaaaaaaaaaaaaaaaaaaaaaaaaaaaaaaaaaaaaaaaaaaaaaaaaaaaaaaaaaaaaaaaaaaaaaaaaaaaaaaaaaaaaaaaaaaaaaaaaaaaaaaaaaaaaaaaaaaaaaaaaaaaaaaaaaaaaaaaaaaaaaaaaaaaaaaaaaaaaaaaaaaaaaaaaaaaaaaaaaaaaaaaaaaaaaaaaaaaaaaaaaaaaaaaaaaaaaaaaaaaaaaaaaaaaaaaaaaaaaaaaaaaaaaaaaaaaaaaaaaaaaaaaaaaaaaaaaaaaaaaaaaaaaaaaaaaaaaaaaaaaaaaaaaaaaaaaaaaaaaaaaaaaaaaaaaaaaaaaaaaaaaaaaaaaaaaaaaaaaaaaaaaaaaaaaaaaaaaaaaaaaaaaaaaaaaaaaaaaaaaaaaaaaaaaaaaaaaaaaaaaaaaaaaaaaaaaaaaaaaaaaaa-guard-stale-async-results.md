---
title: Guard stale async results
description: 'When a hook kicks off an async operation (an RPC/invoke, a promise race,
  a deferred send) whose result will later update state, the component''s context
  can change before that result arrives: the session can rebind, the thread can unmount/remount,
  the user can edit the draft, or newer local state can supersede it. Applying the
  async result blindly causes...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: React
language: TypeScript
comments_count: 5
repository_stars: 70964
---

When a hook kicks off an async operation (an RPC/invoke, a promise race, a deferred send) whose result will later update state, the component's context can change before that result arrives: the session can rebind, the thread can unmount/remount, the user can edit the draft, or newer local state can supersede it. Applying the async result blindly causes race conditions — stale replies overwriting fresher state, duplicate sends, or data bleeding across unrelated sessions/threads.

To avoid this:
- Snapshot the inputs that matter (session id, revision, attached files, run count, etc.) at the moment the action is fired, rather than re-reading live refs/closures inside the `.then`/callback.
- Tag every bind/attach/mount with an incrementing generation (or epoch) counter; capture it before the await and compare it after — discard or re-derive the result if the generation has changed.
- Before using a deferred result to mutate shared state (e.g., restoring a draft, reinserting a prompt), revalidate that the original target is still current (same thread/session/draft) rather than trusting a ref owned by a retired instance.

Example pattern:
```ts
const generationRef = useRef(0);

async function rebind(sessionId: string) {
  generationRef.current += 1;
  const generation = generationRef.current;
  const result = await invoke(sessionId, action);
  if (generation !== generationRef.current) return; // superseded, ignore
  dispatch({ type: "reply", result });
}
```

Apply the same discipline to any "snapshot now, apply later" flow: capture attached files/draft content at send time and reconcile only against what's still true when the verdict lands, and re-check current draft/thread state before restoring a failed/queued action so a retired pane can't clobber newer input.