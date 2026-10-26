---
title: Avoid Duplicate Expensive Work
description: 'Coding standard: treat remote/Git/clipboard/session attachment operations
  as expensive—do them once per user action, reuse their results, and strictly scope
  what you fetch/connect.'
repository: cline/cline#v13
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70874
---

Coding standard: treat remote/Git/clipboard/session attachment operations as expensive—do them once per user action, reuse their results, and strictly scope what you fetch/connect.

Apply this as:
1) Reuse computed snapshots/results across telemetry + UI/message emission (never recapture just to compute a flag).
2) Remove duplicated reads/checks across layers—centralize preflight logic so the repo/network is queried in one place.
3) Scope remote enumeration: list only the minimal refs needed (e.g., upstream/default) instead of fetching every head; prefer local tracking refs when possible.
4) Prevent background connections during hydration/preview flows; only attach/reactivate remote sessions when the user explicitly opens them.
5) For unavoidable async waits behind locks, surface a pending state and coalesce rapid toggles to reduce user-visible stalls.

Example (reuse capture for telemetry):
```ts
async function fallbackCapture(telemetryService: any) {
  // Fetch once
  const terminalSnapshot = await getLatestTerminalOutput();

  // Emit fallback message derived from the same snapshot
  await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);

  // Reuse the same snapshot for success/failure telemetry
  telemetryService.captureTerminalOutputFailure(
    terminalSnapshot.ok ? 'NONE' : 'TIMEOUT'
  );
}
```

Checklist for PRs in this category:
- Are there any expensive calls repeated in different branches (fetch/capture/read-tree/ls-remote/clipboard reads)?
- Is any remote enumeration broader than necessary (all heads, all remotes, deep history)?
- Does background UI hydration trigger network/Hub attachments for items the user hasn’t opened?
- If a UI toggle waits on async work, is there a pending state and are rapid toggles coalesced? 