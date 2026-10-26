---
title: Use Single Source Interfaces
description: When client behavior depends on “who/what the user is” or a special interaction
  mode, avoid duplicating authority via extra API calls. Prefer a single source of
  truth (local provider/model selection) and ensure any remote data you do use has
  consistent fallback semantics with the local path. Additionally, if the client enters
  a special mode (recording,...
repository: cline/cline#v3
label: API
language: TSX
comments_count: 2
repository_stars: 70863
---

When client behavior depends on “who/what the user is” or a special interaction mode, avoid duplicating authority via extra API calls. Prefer a single source of truth (local provider/model selection) and ensure any remote data you do use has consistent fallback semantics with the local path. Additionally, if the client enters a special mode (recording, editing, etc.), gate *all* relevant client entry points behind a shared suspension/state flag so no other handlers run concurrently.

Practical rules:
- Don’t add server “plan/status” checks if the same capability decision is already determined by the local provider/model selection.
- Keep remote-carried models semantically consistent with local models; if a carried model can fail, it should fail the same way the equivalent local model would.
- Centralize “mode” gating (e.g., suspension) and have every related handler consult it; ensure the suspension lifecycle is test-covered.

Example pattern (client gating):
```ts
// Shared state
let suspensionCount = 0;
const isSuspended = () => suspensionCount > 0;

export function suspendShortcuts() { suspensionCount++; }
export function resumeShortcuts() { suspensionCount = Math.max(0, suspensionCount - 1); }
export { isSuspended };

// Any handler that must not run during the mode
function onKeyDown(event: KeyboardEvent) {
  if (isSuspended()) return;
  // normal shortcut handling...
}

// Mode entry
function startRecording() {
  suspendShortcuts();
  // also stop other listeners from seeing the initiating key if needed
  // event.stopImmediatePropagation()
}

// Mode exit
function stopRecording() {
  resumeShortcuts();
}
```