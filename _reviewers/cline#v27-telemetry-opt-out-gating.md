---
title: Telemetry opt-out gating
description: 'When implementing telemetry/tracing, treat user opt-out as a hard security/privacy
  control: check opt-out *before* creating or emitting any spans/events, and ensure
  “record content” or similar flags cannot bypass it.'
repository: cline/cline#v27
label: Security
language: Yaml
comments_count: 1
repository_stars: 70892
---

When implementing telemetry/tracing, treat user opt-out as a hard security/privacy control: check opt-out *before* creating or emitting any spans/events, and ensure “record content” or similar flags cannot bypass it.

**Apply this rule**
- **Fail closed:** if opt-out settings can’t be read/parsed, assume opt-out is enabled.
- **Two-stage behavior:**
  1) If opted out, **return early** (no span creation/emission).
  2) Only if not opted out, apply sampling and then decide whether to record sensitive content.
- **Make opt-out effective promptly:** read the authoritative opt-out configuration per stream/session (not just at process start).

**Pattern (pseudocode)**
```ts
function resolveTelemetry({ settings, samplePercent }) {
  // Stage 1: hard opt-out gate
  if (!settings?.telemetryOptOutOk /* or isTelemetryOptedOutGlobally() */) {
    return { enabled: false }; // no span created
  }

  // Stage 2: only after enabled
  if (Math.random() * 100 > samplePercent) {
    return { enabled: false }; // sampled out
  }

  const recordContent = settings?.recordContent === true; // e.g., CLINE_TRACE_RECORD_CONTENT
  return { enabled: true, recordContent };
}
```

This ensures configuration like `recordContent=true` doesn’t violate user expectations, because it only affects what’s attached *after* tracing is explicitly permitted.