---
title: Respect telemetry opt-out
description: 'When adding or configuring telemetry/tracing, treat user opt-out as
  a security/privacy control—not a display setting. Ensure your implementation:

  - Checks global/user opt-out **before creating any spans** or emitting trace data.'
repository: cline/cline#v28
label: Security
language: Yaml
comments_count: 1
repository_stars: 70893
---

When adding or configuring telemetry/tracing, treat user opt-out as a security/privacy control—not a display setting. Ensure your implementation:
- Checks global/user opt-out **before creating any spans** or emitting trace data.
- Applies flags that increase data collection (e.g., recording prompt/response content) **only after** opt-out is confirmed as allowed.
- Re-reads opt-out state per request/stream (or otherwise ensures toggles take effect promptly).
- Fails **closed**: if opt-out settings can’t be loaded or are corrupt, default to disabling telemetry.

Example pattern (self-contained):
```ts
function resolveTelemetry({ globalOptOut }: { globalOptOut: boolean }) {
  // 1) Enforce opt-out first: do not create spans when opted out.
  if (globalOptOut) return { telemetry: 'disabled' as const };

  // 2) Only after allowed, apply sampling/record-content behavior.
  const samplePercent = Number(process.env.TRACE_SAMPLE_PERCENT ?? '100');
  const recordContent = process.env.TRACE_RECORD_CONTENT === 'true';

  return { telemetry: 'enabled' as const, samplePercent, recordContent };
}
```

Practical checklist for reviews:
- Does the code gate **span creation** behind opt-out?
- Can `record content`/payload flags accidentally override opt-out?
- Is opt-out fetched dynamically (per stream/request), not just read once at startup?
- On config errors, does the behavior default to **disabling** telemetry? 