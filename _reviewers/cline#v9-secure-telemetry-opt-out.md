---
title: Secure telemetry opt-out
description: When adding telemetry/tracing (especially anything that could include
  user prompts, responses, or other sensitive content), enforce privacy as a first-class
  security control.
repository: cline/cline#v9
label: Security
language: Yaml
comments_count: 1
repository_stars: 70868
---

When adding telemetry/tracing (especially anything that could include user prompts, responses, or other sensitive content), enforce privacy as a first-class security control.

**Standard**
- **Check user opt-out before creating any spans**: if opted out, produce **no spans/events**.
- **Gate sensitive content separately**: flags like `recordInputs`/`recordOutputs` (e.g., `CLINE_TRACE_RECORD_CONTENT`) must only control *whether content is attached after tracing is allowed*.
- **Apply decisions in the correct order**: `opt-out → sampling → record-content`.
- **Honor changes promptly**: re-read opt-out settings for each stream/request so toggles take effect mid-session.
- **Fail closed**: if opt-out config is missing/corrupt/unreadable, default to opted-out behavior.

**Example pattern**
```ts
function resolveTelemetryConfig(settings: Settings) {
  // 1) Fail closed + opt-out before any span
  if (settings.isTelemetryOptedOutGlobally()) {
    return { tracingEnabled: false };
  }

  // 2) Sampling
  const sampled = Math.random() < settings.clineTraceSamplePercent / 100;
  if (!sampled) return { tracingEnabled: true, recordContent: false };

  // 3) Only now decide whether to record sensitive content
  const recordContent = settings.get('CLINE_TRACE_RECORD_CONTENT') === 'true';
  return { tracingEnabled: true, recordContent };
}
```

This prevents accidental collection of user data even if content-recording flags are enabled, aligning telemetry behavior with user privacy/security expectations.