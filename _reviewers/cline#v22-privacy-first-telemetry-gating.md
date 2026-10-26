---
title: Privacy-first telemetry gating
description: 'When adding tracing/telemetry that may capture user content, ensure
  the implementation is privacy-safe: an explicit opt-out must prevent span creation
  and must be evaluated before any “record content” behavior.'
repository: cline/cline#v22
label: Security
language: Yaml
comments_count: 1
repository_stars: 70886
---

When adding tracing/telemetry that may capture user content, ensure the implementation is privacy-safe: an explicit opt-out must prevent span creation and must be evaluated before any “record content” behavior.

Apply this standard:
- **Opt-out first (fail closed):** Check `isTelemetryOptedOutGlobally()` (or equivalent) before creating spans or enabling any recording.
- **Subordinate content flags:** Treat flags like `CLINE_TRACE_RECORD_CONTENT` as *only* controlling whether inputs/outputs are attached **after** opt-out passes.
- **Sampling after opt-out:** Apply sampling only after opt-out has allowed tracing.
- **Re-read opt-out frequently:** Re-check opt-out settings per stream/session so user toggles take effect immediately.
- **Robustness:** If opt-out configuration is unreadable/corrupt, default to opted-out (disable telemetry).

Example pattern (structure):
```ts
const { optedOut, recordContent } = getTelemetryPolicy();
if (optedOut) return { status: 'TELEMETRY_DISABLED' }; // no span created
if (!shouldSample()) return { status: 'NOT_SAMPLED' };
const recordInputs = recordContent;
const recordOutputs = recordContent;
// create span with input/output recording only when opt-out is false
```
This prevents hardcoded “record content” flags from becoming an opt-out bypass, aligning telemetry behavior with user privacy expectations (Security/Privacy best practice).