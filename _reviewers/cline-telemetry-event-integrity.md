---
title: Telemetry event integrity
description: Treat telemetry as data that other code and dashboards depend on, not
  as scattered debug prints. Register every new event in the central catalog (e.g.
  `CORE_TELEMETRY_EVENTS`) with a typed `captureX` helper instead of calling `.capture()`
  with a raw string literal or ad-hoc properties — this keeps names consistent and
  is enforced by catalog-consistency...
repository: cline/cline
label: Observability
language: TypeScript
comments_count: 10
repository_stars: 70886
---

Treat telemetry as data that other code and dashboards depend on, not as scattered debug prints. Register every new event in the central catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX` helper instead of calling `.capture()` with a raw string literal or ad-hoc properties — this keeps names consistent and is enforced by catalog-consistency tests. When a helper's parameters change (e.g. a `taskId` renamed to `ulid`), update every call site; a positional rename that type-checks but silently passes the wrong value corrupts the property's meaning across all historical events. Choose failure/reason codes that actually match the observed condition instead of reusing a convenient existing one (e.g. don't report an "empty output" case as `TIMEOUT`, and don't label every `ask` rejection as a `STREAM_TIMEOUT` hang) — misclassification pollutes the metric and defeats the purpose of having distinct reasons. For multi-phase operations, always pair a `started` event with a terminal `completed`/`failed` phase on every code path, including throws and aborts, so dashboards never show orphaned "started" events; keep such telemetry purely observational (state what happened, e.g. `retried` with the observed finish reason) rather than duplicating business-logic verdicts that the calling code is responsible for. Avoid double-instrumenting an action that is already captured centrally (e.g. tool usage emitted once via the runtime's event pipeline) to prevent double-counting. Finally, when an instrumentation path hits a resource limit (size/time), prefer emitting a degraded/partial signal over dropping the whole observation, so expensive-but-rare events (large repos, big diffs) still contribute some visibility instead of silently vanishing.