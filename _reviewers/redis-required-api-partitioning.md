---
title: Required API Partitioning
description: When designing cluster APIs/specs, explicitly partition endpoints into
  categories by *actor* and *compatibility obligation*, and document which categories
  alternative implementations must implement.
repository: redis/redis
label: API
language: Markdown
comments_count: 4
repository_stars: 74261
---

When designing cluster APIs/specs, explicitly partition endpoints into categories by *actor* and *compatibility obligation*, and document which categories alternative implementations must implement.

**Standard**
1. **Define the compatibility surface** (what non-admin clients and core node behavior need). Mark these endpoints as **Required**.
2. **Separate reference/admin orchestration** (what operators use to create/configure/manage entities). Mark these as **Admin/Optional**.
3. **Keep internal control-plane comms** (e.g., TD↔FC status propagation) out of the external compatibility surface. Mark these as **Internal/Not Required**.
4. For any advanced controls (e.g., externally imposed shard identity), ensure the **default flow remains ergonomic**, and treat identity/placement parameters as **opt-in options** on the required or admin interfaces.

**Practical checklist**
- For each command/endpoint, label: `{Actor: node|client|admin|internal, Obligation: Required|Optional|Not Required}`.
- Add a short compatibility statement: “Any alternative implementation that claims drop-in compatibility MUST implement all *Required* endpoints (optionally subsets), but may ignore *Internal/Not Required* endpoints.”
- Ensure optional power-user fields (e.g., `shard_id`) are not required for the default path.

**Example (shape of the spec, pseudo-code)**
```text
Endpoint: HEARTBEAT
  Actor: node
  Obligation: Required
  Purpose: node↔FC liveness, role decisions

Endpoint: TD/FC internal messages (FAILOVER_STATUS, TOPology_RESPONSE)
  Actor: internal
  Obligation: Not Required
  Purpose: FC↔TD propagation; no compatibility guarantee

Endpoint: ADMIN.CREATE_SHARD / SHARD_ID on NODE_JOIN
  Actor: admin
  Obligation: Optional
  Default: shard IDs auto-managed
  Power-user: allow specifying shard_id to match external orchestration needs
```
This prevents “spec creep” where admin/internal endpoints accidentally become de-facto requirements, and it allows alternative implementations to remain compatible without re-creating internal details.