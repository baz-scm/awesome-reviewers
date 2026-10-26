---
title: Telemetry Integrity Checklist
description: 'Enforce telemetry that is accurate, contract-compliant, and isolated
  from runtime semantics.


  Apply these rules whenever adding/updating metrics, tracing, or telemetry events:'
repository: cline/cline#v9
label: Observability
language: TypeScript
comments_count: 13
repository_stars: 70868
---

Enforce telemetry that is accurate, contract-compliant, and isolated from runtime semantics.

Apply these rules whenever adding/updating metrics, tracing, or telemetry events:

1) **Don’t let observers mutate core/session identity**
- Telemetry should attach hooks and report, not rewrite bootstrap config (e.g., sessionId, restart signals).

2) **Prevent false samples with correct cleanup**
- If you arm observation windows/timers, cancel them on all early-exit paths (e.g., spawn failures). Otherwise you’ll emit “exited:false after N seconds” for a process that never started.

3) **Guarantee lifecycle phase correctness**
- For any `started`/`ended` telemetry lifecycle, ensure there is always a terminal phase on *all* paths (success, expected failure, abort, and “listener/hook threw”). If spans/tracing end in another callback, record the error before the span closes.

4) **Use accurate categorization/attribution**
- Reset/clear attribution per the correct scope (turn vs run). Don’t clear provider details except for the specific failure that ended the run.
- Emit the correct failure reason (timeout vs empty output vs ask error). Mislabels degrade metric usefulness.

5) **Avoid double-counting**
- If the event is already produced centrally (adapter/runtime/task pipeline), don’t re-emit it in downstream handlers.

6) **Follow event naming/data contracts + sanitization**
- Use typed event catalogs/constants/helpers where required; don’t embed raw event strings in scoped packages.
- Never export prompt text or other sensitive fields; drop or hash safely according to the host’s sanitization rules.

Example (phase/cleanup pattern):
```ts
let timer: NodeJS.Timeout | undefined;
let reported = false;

function reportOnce(payload: { durationMs: number; exited: boolean }) {
  if (reported) return;
  reported = true;
  if (timer) clearTimeout(timer);
  capture({ event: "...", properties: payload });
}

try {
  if (detached) {
    timer = setTimeout(() => reportOnce({ durationMs: N, exited: false }), N);
    void completed.then(r => reportOnce({ durationMs: Date.now() - startedAt, exited: true }));
  }
} catch (e) {
  // Critical: cancel observation window on spawn/arm failure
  if (timer) clearTimeout(timer);
  throw e;
}
```

When you review a PR, verify each telemetry change against all six rules above (at least 1/6 is acceptable for tiny changes, but larger/branchy changes must satisfy 3–6).