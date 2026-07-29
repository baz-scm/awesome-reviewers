---
title: Typed API Contracts
description: When introducing or changing an API seam (hooks, callback payloads, lifecycle
  state transitions), require an explicit, end-to-end, type-safe contract that matches
  implementation and documentation.
repository: QwenLM/qwen-code
label: API
language: Markdown
comments_count: 6
repository_stars: 26407
---

When introducing or changing an API seam (hooks, callback payloads, lifecycle state transitions), require an explicit, end-to-end, type-safe contract that matches implementation and documentation.

Checklist:
- **Define the shared contract in code**: provide a minimal TS interface/type for any referenced context object (field names + responder signature), not prose-only descriptions.
- **Propagate correlation IDs end-to-end**: if callbacks/actions must target an exact in-flight entity (e.g., Stop for a specific run), the required token (e.g., `runId`) must be carried through the shared event/callback payload chain, not stored only in adapter-private state.
- **Eliminate “any” for dispatch-critical semantics**: don’t encode state in fields like `AbortSignal.reason` (typed as `any` in practice). Route settlement through a typed helper/callback so misspellings can’t compile.
- **Sync docs to the real exported API**: method signatures, parameter lists, and which hook delivers which data must match the actual implementation; if segment/reason is delivered via a different hook, document that explicitly.
- **Align state names with existing lifecycle events**: if the system doesn’t have a real terminal event (e.g., no `stopped` event), require an explicit mapping table or explicit statement of how the state is derived.

Example pattern (typed settlement wrapper):
```ts
type UserInputSettlementReason =
  | 'resolved_outside_card'
  | 'request_cancelled'
  | 'run_cancelled'
  | 'expired';

function setSettlementReason(signal: AbortSignal, reason: UserInputSettlementReason) {
  // avoid writing to any-typed fields directly; centralize the mapping
  (signal as any).__settlementReason = reason;
}
```

Example contract sketch (adapter-facing context):
```ts
interface ChannelUserInputRequestContext {
  requestId: string;
  sessionId: string;
  runId: string;
  target: SessionTarget;
  ownerId: string;
  request: PermissionRequestEvent['request'];
  settlementSignal: AbortSignal;
  respond(response: { /* RequestPermissionResponse + optional answers */ }): Promise<boolean>;
}
```

If any of the above can’t be satisfied, treat it as an API design bug: either the contract is incomplete, the correlation is not end-to-end, the semantics are not type-safe, or the documentation/API surface are out of sync.