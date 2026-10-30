---
title: Telemetry event integrity
description: 'Treat telemetry as data that must stay trustworthy and actionable, not
  just "something fired":


  1. Route every first-party event through the central typed catalog (e.g. `CORE_TELEMETRY_EVENTS`
  / a shared constants module) with a typed capture helper, instead of inlining raw
  event-name strings. Add/extend a catalog-consistency test when introducing a new...'
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Observability
language: TypeScript
comments_count: 9
repository_stars: 71067
---

Treat telemetry as data that must stay trustworthy and actionable, not just "something fired":

1. Route every first-party event through the central typed catalog (e.g. `CORE_TELEMETRY_EVENTS` / a shared constants module) with a typed capture helper, instead of inlining raw event-name strings. Add/extend a catalog-consistency test when introducing a new event. Example: a new lifecycle event should be exported as a shared constant, added to the catalog object, and wrapped in a `captureX()` helper rather than called as `telemetry.capture({ event: "some.raw.string" })` ad hoc.

2. Make sure the value reported actually matches the condition being observed. Don't reuse an existing enum value (e.g. reporting `TIMEOUT` for what is really an "empty output" case) or a stale/renamed field (e.g. sending a `taskId` value under a `ulid` property after a rename) — these corrupt the metric and are invisible to the type checker because parameters are positional. When a property is renamed or a new failure reason is introduced, update every call site and prefer deriving the value from the actual event/outcome being recorded (e.g. the current turn/response) rather than assuming the last item in some mutable transcript/state reflects what happened.

3. Avoid double-instrumenting the same underlying action from multiple layers (e.g. capturing tool usage both in a tool handler and in the central event pipeline that already emits it); keep one authoritative emission point and add a regression test asserting the event fires exactly once.

4. Before adding a new metric/event, be able to state concretely how it will be used — a dashboard, a specific decision gate, incident investigation, or a tripwire for a known failure mode — and keep its scope/cardinality narrow and bounded to that purpose. If nothing ends up consuming it, remove it.

5. When an event's phase/state naming could be read as asserting a verdict the component doesn't actually own (e.g. "completed" implying success when a downstream loop still decides acceptability), name it neutrally (e.g. "retried") and document what it does and does not claim.

Applying these checks during review turns telemetry into a reliable source for dashboards, debugging, and alerting instead of a liability of misleading or duplicated data.