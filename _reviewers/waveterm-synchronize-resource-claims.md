---
title: Synchronize resource claims
description: 'When asynchronous operations cross process or component boundaries (backend
  <> frontend, websocket events, UI lifecycle), design explicit synchronization instead
  of relying on ad-hoc timing. Apply these rules:'
repository: wavetermdev/waveterm
label: Concurrency
language: TypeScript
comments_count: 3
repository_stars: 17328
---

When asynchronous operations cross process or component boundaries (backend <> frontend, websocket events, UI lifecycle), design explicit synchronization instead of relying on ad-hoc timing. Apply these rules:

- Prefer authoritative coordination: move critical claim/transfer logic to the authoritative service (backend). Operations that modify ownership (delete workspace, transfer window ownership) should be atomic and return an explicit result the client can act on (e.g., replacementId or empty). The client should only perform follow-up actions after receiving that result.

  Example (pseudo):
  // server: atomically choose replacement or clear owner and return id or empty string
  func DeleteWorkspace(id) -> string {
    if findReplacementForWindow(ownerWindow) {
      claimReplacement(replacementId, ownerWindow)
      return replacementId
    }
    cleanupWindowOwner(ownerWindow)
    return ""
  }

  // client: act only on server response
  const replacement = await WorkspaceService.DeleteWorkspace(workspaceId)
  if (replacement) {
    await switchWorkspace(replacement)
  } else {
    window.destroy()
  }

- If some coordination must remain client-side, use explicit coordination primitives not blind delays: prefer promises/events/component-ready hooks over setTimeout. Only use timeouts as a fallback when no readiness signal exists.

  Example (UI focus):
  // prefer event-driven readiness
  await sessionView.ready()
  inputModel.giveFocus()

  // fallback only if necessary
  setTimeout(() => inputModel.giveFocus(), 50)

- For out-of-order or eventual-consistency events (e.g., websocket update before add), implement bounded retries with short delay/backoff and a clear failure path. Log retries and abort after N attempts to avoid infinite loops.

  Example (retry for missing line):
  async function ensureLineAndApply(lineId, update) {
    for (let attempt=0; attempt<5; attempt++) {
      if (lines[lineId]) { lines[lineId].apply(update); return }
      await sleep(100 * (attempt+1)) // small backoff
    }
    console.warn(`Failed to find line ${lineId} after retries`)
  }

- General rules: use compare-and-swap or explicit claim APIs when possible; bound retries and timeouts; make failure modes observable (logs/metrics); write tests for race scenarios.

Motivation: these practices prevent races between concurrent actors, make system behavior deterministic, and move complex invariants into the authoritative layer where they can be enforced reliably. References: discussions on workspace deletion/claim races (0), UI focus timing (1), and websocket update ordering with retry (2).