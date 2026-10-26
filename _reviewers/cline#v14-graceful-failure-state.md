---
title: Graceful Failure State
description: 'When UI depends on async actions or external/runtime availability, design
  failure paths to be deterministic: preserve user state, reuse the canonical “blocked/error”
  UX, and recover the UI to a known-good view without leaking listeners/styles.'
repository: cline/cline#v14
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70876
---

When UI depends on async actions or external/runtime availability, design failure paths to be deterministic: preserve user state, reuse the canonical “blocked/error” UX, and recover the UI to a known-good view without leaking listeners/styles.

Practical standards
- Success-gate state changes: only clear/commit user input after the underlying action definitively succeeds. If the action fails/rejects, keep the current draft/message/attachments intact.
- Reuse the primary guard UX: if an action is blocked (read-only, missing capability/model, etc.), run the same pre-send checks as the main flow and display the same toast/error as the canonical path.
- Replace with the correct recovery screen: for critical component startup failures, render the recovery UI instead of leaving the app mounted-but-broken or merely overlaying controls.
- Make cleanup resilient to missed events: if relying on browser events for teardown (drag resize, pointer interactions), also detect “release without pointerup” and ensure listeners/styles are restored.

Example pattern (success-gated async UI)
```ts
async function onConfirmCommit() {
  // compute payload from current message
  const ok = await onAction({ type: "commit", message: message.trim(), push });
  if (!ok) {
    // show toast/error via the same path; do NOT clear message
    return;
  }
  setMessage(""); // only on success
}
```

Example pattern (blocked action keeps draft)
```ts
async function onSendFromTray() {
  const blocked = await composerCanSendChecks(/* draft/model/repo/etc */);
  if (blocked) {
    // show the canonical toast; do not mutate draft/attachments
    return;
  }
  await composerSend();
}
```

Example pattern (deterministic cleanup for missed pointerup)
```ts
function onMove(e: PointerEvent) {
  // If release happened outside and no pointerup fired, end drag on next move
  if (!e.buttons) {
    restoreBodyStylesAndRemoveListeners();
    return;
  }
  updateHeight();
}
```