---
title: Bound Hot-Path Work
description: When code runs on hot UI paths (keystrokes, popup open, navigation) or
  retains state for long-lived sessions, enforce **bounded work** and **targeted updates**.
repository: microsoft/VSCode
label: Performance Optimization
language: TypeScript
comments_count: 10
repository_stars: 194303
---

When code runs on hot UI paths (keystrokes, popup open, navigation) or retains state for long-lived sessions, enforce **bounded work** and **targeted updates**.

Practical rules:
1) **Bound retained state**: Correlation maps, caches, and storage histories must be cleaned when the owning operation completes/discards; prefer per-item/turn cleanup over scanning unbounded maps.
2) **Avoid synchronous whole-document work on input**: Keystrokes should only query already-available lightweight data. If tree/indexing is required, do it asynchronously or lazily after the user pauses.
3) **Cap large DOM/ARIA previews**: Never assign unbounded diagnostic/error bodies into the layout/measurement path. Render a small capped preview and load/expand full text only on explicit user action.
4) **Prefer incremental DOM updates over full rebuilds/remeasurements**: Don’t clear and recreate large containers on frequent “status” events. Subscribe narrowly (per row) and invalidate only what changed.
5) **Deduplicate/coalesce repeated background work**: If navigation happens within the same lifecycle, don’t recompute session-wide assessments or re-run probes—schedule once per true lifecycle transition (or memoize per active entry).
6) **Lazy-instantiate heavy widgets**: Don’t construct Monaco/code editor widgets or run layout on modal creation; create them only when the user actually opens the relevant pane/details.

Example (cleanup bounded correlation on completion):
```ts
// Keep only correlations relevant to the active host turn.
// Cleanup on completion/discard prevents heap growth.
private _hostTurnIdsBySdkTurnId = new Map<string, string>();
private _hostTurnIdsByInteractionId = new Map<string, string>();

private _onProtocolTurnCompleted(turnId: string, interactionId?: string) {
  // Remove only entries created for this turn.
  const sdkTurnId = this._findSdkTurnIdForHost(turnId); // or store reverse key per turn
  if (sdkTurnId) {
    this._hostTurnIdsBySdkTurnId.delete(sdkTurnId);
  }
  if (interactionId) {
    this._hostTurnIdsByInteractionId.delete(interactionId);
  }
}
```

Use this standard to review changes that add AST/indexing queries, telemetry/computation, Monaco/widget creation, accessibility scans, list/card refresh logic, or diagnostic rendering—especially when failures, large payloads, or many items are possible.