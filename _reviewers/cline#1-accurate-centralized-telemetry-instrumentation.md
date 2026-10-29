---
title: Accurate, centralized telemetry instrumentation
description: 'Telemetry events must be trustworthy, non-duplicated, and complete,
  or dashboards built on them will mislead.


  - Catalog, don''t inline: register every first-party event under the shared catalog
  (e.g. `CORE_TELEMETRY_EVENTS.<DOMAIN>.<EVENT>`) with a typed `captureX`/`recordX`
  helper, instead of passing raw event-name strings or ad-hoc property bags at the...'
repository: cline/cline#1
label: Observability
language: TypeScript
comments_count: 13
repository_stars: 71024
---

Telemetry events must be trustworthy, non-duplicated, and complete, or dashboards built on them will mislead.

- Catalog, don't inline: register every first-party event under the shared catalog (e.g. `CORE_TELEMETRY_EVENTS.<DOMAIN>.<EVENT>`) with a typed `captureX`/`recordX` helper, instead of passing raw event-name strings or ad-hoc property bags at the call site. This keeps event names, property shapes, and sanitization consistent and lets a single lint rule catch drift. Sandboxed/plugin or third-party telemetry that is renamed/namespaced by the host before export is out of scope for the core catalog, but should still go through its own typed helper.
- Instrument once, at the authoritative layer: before adding a new capture call, check whether the event is already emitted from a shared pipeline (e.g. a central event adapter). Adding a second call site at a different layer causes double-counting.
- Make the reported reason match the real condition: a failure's classification (e.g. `TIMEOUT` vs `NO_OUTPUT`, `STREAM_TIMEOUT` vs `ASK_FAILED`) must reflect what actually happened, not just the nearest existing enum value — add a new reason/stage if none fits. When renaming a property (e.g. `taskId` → `ulid`), update every call site and verify the value's semantics actually changed, since positional-argument renames compile cleanly even when they silently send the wrong data.
- Close every lifecycle you open: if an operation emits a `started` phase, every exit path — success, expected failure, abort, and thrown/rethrown error — must emit a matching terminal phase (`succeeded`/`failed`/etc.) before propagating, so counts of `started` and terminal outcomes always reconcile.
- Keep telemetry observational, not a second decision-maker: lifecycle/recovery telemetry should report facts about what ran (e.g. "retry attempted, finish reason X"), not re-derive a success/failure verdict that the main control flow already owns — duplicating that logic in two places lets them drift.
- For tracing, ensure a span's terminal status/exception is set before the span closes; an error reported only after the span's lifecycle has ended cannot be attached to it.
- Before adding a new event, state what question or dashboard it will answer and keep its volume/content bounded — unused or unbounded events should be avoided or removed.