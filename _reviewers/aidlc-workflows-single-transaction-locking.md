---
title: Single-Transaction Locking
description: 'For any shared mutable system state (receipts/ledgers, stage files +
  sidecars, and derived artifacts), treat the operation as one transaction: acquire
  a single shared lock, perform all read/validate/merge/emit/write steps (and any
  dependent compile/derivation) while holding it, then release.'
repository: awslabs/aidlc-workflows
label: Concurrency
language: TypeScript
comments_count: 5
repository_stars: 3849
---

For any shared mutable system state (receipts/ledgers, stage files + sidecars, and derived artifacts), treat the operation as one transaction: acquire a single shared lock, perform all read/validate/merge/emit/write steps (and any dependent compile/derivation) while holding it, then release.

Also enforce state-machine invariants inside that same critical section (e.g., refuse to reopen a completed unit, or ensure checkpoint/receipt consistency can’t be contradicted by a concurrently written receipt).

Do NOT:
- Perform “check-and-consume” across separate operations without holding the lock across the check + append + state update.
- Lock only the final compile step while leaving earlier read/merge/write steps unprotected.
- Use different locks for related workflows that touch the same artifacts (e.g., selection changes and compose must share the same lock).
- Mutate shared committed directories in parallel tests; isolate writes via temp/outDir seams.

Example (pattern):
```ts
withAuditLock(pd, () => {
  const content = readStateFile(pd);

  // validate against current ledger/state
  if (isAutonomousMode(content)) throw new Error('...');
  if (action === 'start' && /* would reopen completed */) throw new Error('...');

  // consume/append/merge/update while still locked
  appendAuditReceipt(pd, { type: 'AUTONOMY_MODE_SET', ... });
  writeStateFile(pd, newContent);

  // include dependent writes/derivations in the same transaction
  composeStageAndSidecar(pd, { mergeScopes: true });
  compileGraph(pd);
});
```

Outcome: no interleaving can cause double-consumption, lost merges, or orphaned scope membership; and correctness checks remain consistent with the single snapshot seen under the lock.