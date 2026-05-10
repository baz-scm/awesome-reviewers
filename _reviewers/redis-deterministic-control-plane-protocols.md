---
title: Deterministic Control-Plane Protocols
description: When multiple agents participate in cluster control-plane updates (e.g.,
  TD, FC, nodes), treat the protocol as an algorithm and make its conflict-resolution
  and time/progression semantics explicit in the spec/code review contract.
repository: redis/redis
label: Algorithms
language: Markdown
comments_count: 4
repository_stars: 74261
---

When multiple agents participate in cluster control-plane updates (e.g., TD, FC, nodes), treat the protocol as an algorithm and make its conflict-resolution and time/progression semantics explicit in the spec/code review contract.

**Standards**
1) **Define a strict authority hierarchy (deterministic winner).** If agents can reject or delay configs (e.g., FC rejects “invalid” topology), the spec must state what happens in disagreement and who has the final vote (e.g., TD decides topology metadata; FC decides primary/replica status). Avoid designs where an agent bug can permanently wedge the system.
2) **Define recovery contracts, not just “fix bugs.”** Specify what the system does if validation fails or messages arrive out of order, including anti-deadlock guarantees and how to un-wedge (e.g., force flags, admin-driven reconciliation).
3) **Use monotonic progression signals for all time-based decisions.** Do not rely on multiple unsynchronized clocks across components. Have the control-plane coordinator maintain a monotonically increasing counter (tick) and include it in responses so nodes can compute “time since last primary update” from tick deltas.
4) **Separate validation from decision responsibilities.** Keep validation scope tight and named: for example, FC can validate epoch correctness and ownership/ownership changes, while nodes perform failover triggering based on the FC-provided state and tick-based timeouts.
5) **Enforce critical invariants to prevent state-space races.** Example invariant: no concurrent updates for the same shard until prior epochs are acknowledged by all relevant nodes/FCs.

**How to apply (pseudo-code)**
```pseudo
// Coordinator-provided monotonic tick included in every response
on FC.heartbeat(node_id, node_epoch, shard_epoch):
  if node_epoch < current_epoch: return NACK
  if node_shard_coordinator(node_id) != this.FC_id:
    return MOVED(target_FC_id)
  record(node_id, role, shard_epoch, replication_offset, tick=current_tick)
  return ACK(current_topology_if_needed, shard_results, tick_per_node)

// Node uses FC tick deltas to decide failover (no local multi-clock dependence)
on node.tick_based_timeout_primary_missing(primary_id):
  last_primary_tick = tick_from_FC(primary_id)
  if current_tick_from_FC - last_primary_tick > N:
     if node_is_most_up_to_date_replica():
        propose_promote(role=PRIMARY, bump(shard_epoch))
```

**Review checklist**
- Can we point to the exact “winner rule” in every disagreement case?
- Is there an explicit anti-deadlock/un-wedging plan for invalid or rejected updates?
- Are all timeout/failover decisions derived from coordinator-provided monotonic counters?
- Does each component validate only what it should, and does every decision-maker know its inputs?
- Are concurrency/race invariants (like “no concurrent updates per shard until acknowledged”) stated and enforced? 