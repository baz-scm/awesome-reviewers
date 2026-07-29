---
title: Group-aware Pagination
description: When the client needs a logical unit (run/history group, full resource
  state), the API must paginate and update in a way that preserves that unit across
  requests.
repository: maximhq/bifrost
label: API
language: TSX
comments_count: 3
repository_stars: 6862
---

When the client needs a logical unit (run/history group, full resource state), the API must paginate and update in a way that preserves that unit across requests.

Apply this standard:
1) **Pagination must align to domain groups**
   - If records must be reconstructed into “runs” (or any parent/group), **paginate by the group key** (e.g., `webhook_id`/run) and return the group’s children together.
   - Don’t rely on client-side heuristics to reassemble groups when groups can straddle page boundaries; that will be incorrect whenever boundaries split a group.

   Example contract shape (conceptual):
   - Instead of: `GET /deliveries?limit=25&offset=...` returning *attempts*
   - Prefer: `GET /deliveryRuns?endpointId=...&limit=...&cursor=...` returning runs:
     ```ts
     type DeliveryRun = { runId: string; webhookId: string; attempts: WebhookDelivery[] }
     type DeliveryRunsResponse = { items: DeliveryRun[]; nextCursor?: string }
     ```

2) **Update semantics must be explicit + concurrency-safe**
   - If the API uses full-state `PUT` without a revision/ETag, document that **it is overwrite-by-replace** and that clients must send the complete resource state.
   - If concurrent edits/updates are possible, support **optimistic concurrency** (e.g., `ETag` + `If-Match`) so clients can avoid accidental lost updates.

3) **Don’t export incorrect invariants to the UI**
   - The UI should be able to trust that what it receives is already consistent for the domain view (e.g., each run is whole), rather than attempting best-effort reconstruction across pagination and polling offsets.