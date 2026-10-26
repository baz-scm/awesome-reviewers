---
title: Telemetry opt-out enforcement
description: 'When adding or changing telemetry/tracing, treat privacy controls as
  security-critical: the user’s opt-out must *prevent data collection at the span
  level*, not merely hide certain fields. Also ensure a safe evaluation order and
  fail-closed behavior.'
repository: cline/cline#v30
label: Security
language: Yaml
comments_count: 1
repository_stars: 70894
---

When adding or changing telemetry/tracing, treat privacy controls as security-critical: the user’s opt-out must *prevent data collection at the span level*, not merely hide certain fields. Also ensure a safe evaluation order and fail-closed behavior.

Apply this rule:
1) **Gate early**: check global/user opt-out *before creating any span or emitting telemetry*. If opted out, return “disabled” and do not start tracing.
2) **Order matters**:
   - Opt-out check first
   - Sampling second
   - Content recording (e.g., prompt/response bodies) last
3) **Fail closed**: if the settings/config for opt-out is missing, unreadable, or corrupt, assume **opted out**.
4) **Dynamic respect (preferred)**: re-read opt-out settings per stream/request so toggles take effect without restart.

Example (pattern):
```ts
function resolveTelemetry({ globalSettings }) {
  // 1) Opt-out must disable span creation
  if (isTelemetryOptedOutGlobally(globalSettings)) {
    return { telemetry: 'disabled' };
  }

  // 2) Sampling
  const sampled = Math.random() * 100 < Number(process.env.CLINE_TRACE_SAMPLE_PERCENT ?? 0);
  if (!sampled) return { telemetry: 'sampled-out' };

  // 3) Record content only after allowed
  const recordContent = (process.env.CLINE_TRACE_RECORD_CONTENT ?? 'false') === 'true';
  return { telemetry: 'enabled', recordInputsOutputs: recordContent };
}
```

Workflow consistency: if you enable trace exporting (e.g., `OTEL_TRACES_EXPORTER: otlp`) and optionally record content (e.g., `CLINE_TRACE_RECORD_CONTENT: "true"`), confirm that opt-out enforcement still happens first and that the system fails closed when opt-out settings can’t be read.