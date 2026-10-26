---
title: Telemetry opt-out enforcement
description: For any telemetry/tracing that may capture user data, ensure the user’s
  opt-out is enforced before any span/event is emitted. Treat “record content” or
  similar flags as secondary controls that only affect what data is attached after
  tracing is allowed.
repository: cline/cline#v10
label: Security
language: Yaml
comments_count: 1
repository_stars: 70869
---

For any telemetry/tracing that may capture user data, ensure the user’s opt-out is enforced before any span/event is emitted. Treat “record content” or similar flags as secondary controls that only affect what data is attached after tracing is allowed.

Apply this rule by:
- Ordering logic: (1) check global opt-out → if opted out, return without creating spans; (2) apply sampling; (3) read “record content”/data attachment flags.
- Re-checking: read opt-out settings for each stream/request so toggles take effect mid-session.
- Fail-closed: if telemetry settings are missing/corrupt/unreadable, default to opted-out (i.e., create no spans).

Example pattern:
```ts
function resolveAiSdkTelemetry({ settings, samplePercent, recordContentFlag }) {
  // 1) Enforce opt-out first: create no spans at all
  if (settings.isTelemetryOptedOutGlobally()) {
    return { telemetry: 'DISABLED' };
  }

  // 2) Sampling next
  const shouldSample = Math.random() * 100 < samplePercent;
  if (!shouldSample) return { telemetry: 'DISABLED' };

  // 3) Only then decide whether to attach prompt/response content
  const recordInputsOutputs = recordContentFlag === true;
  return {
    telemetry: 'ENABLED',
    recordInputs: recordInputsOutputs,
    recordOutputs: recordInputsOutputs,
  };
}
```
This prevents privacy bypasses where “record content” is hardcoded/enabled but the user has opted out, which is a security/privacy best practice.