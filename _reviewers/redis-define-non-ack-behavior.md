---
title: Define Non-Ack Behavior
description: 'For any control-plane action that depends on acknowledgement (epochs/status
  updates, joins/removes, metadata propagation), the codebase must explicitly define
  end-to-end error handling: timeout, retry/escalation, cascade effects, and the operator
  override path.'
repository: redis/redis
label: Error Handling
language: Markdown
comments_count: 3
repository_stars: 74261
---

For any control-plane action that depends on acknowledgement (epochs/status updates, joins/removes, metadata propagation), the codebase must explicitly define end-to-end error handling: timeout, retry/escalation, cascade effects, and the operator override path.

Apply this standard by ensuring each such operation documents/implements:
1. **Non-ack contract**: what the system does when a target node (or FC/TD hop) never acknowledges (stop progress, keep serving with defined mode, or mark entities unavailable).
2. **Timeout and retry strategy**: exact thresholds and backoff; whether retries continue indefinitely or transition to an escalated state.
3. **Cascade/feedback clarity**: whether non-ack at the node level affects TD/other components, and what errors are propagated upward.
4. **Operator override**: if an escape hatch exists, define a *safe default* (refuse or limit impact) and a *forced* path with prominent warnings and justification.
5. **Troubleshooting path**: a dedicated “everything is broken”/unwedging procedure, including what signals/metrics/errors to look for.
6. **Recovery-mode correctness**: distinguish **automatic recovery** from **rejoin required** when persistence/durability expectations aren’t met; avoid wording that implies guarantees the system doesn’t actually provide.
7. **Admin guardrails for unsafe actions**: when removal/failover can be destructive (e.g., removing a primary), require safer sequencing (failover first, then remove) or ensure force flags are clearly constrained; optionally support client-safe mitigation like connection draining/rotation.

Example (pseudocode pattern for non-ack handling):
```pseudo
function applyTopologyChange(change, targetNode, basedEpoch):
  reqId = newReqId()
  sendRequest(targetNode, change, basedEpoch, reqId)

  deadline = now() + ACK_TIMEOUT
  attempts = 0
  while now() < deadline and attempts < MAX_RETRIES:
    status = waitForAck(reqId, minRemainingTime())
    if status == ACKED and status.epoch == basedEpoch:
      return OK
    attempts++

  // Escalation (defined behavior)
  markEntity(DEGRADED, reason="no ack", epoch=basedEpoch)
  propagateUpstreamIfNeeded(reason="no ack")
  logError(warn="Operation not acknowledged; escalation to operator required", reqId)

  if operatorOverrideEnabled and operatorConfirmed:
    applyForced(change)
  else
    return ERROR("non-ack timeout; operation refused by contract")
```

This turns ambiguous failure modes into deterministic, testable behavior and ensures operators have a clear, warned path to recover when the normal acknowledgement-based workflow cannot complete.