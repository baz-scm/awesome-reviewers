---
title: Error Handling Guardrails
description: 'Adopt a small set of guardrails for failures so recovery is predictable,
  repeatable, and doesn’t deadlock or mask outcomes:


  1) Classify errors into “retryable” vs “permanent,” then apply a bounded retry budget.'
repository: openai/codex-security
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 9394
---

Adopt a small set of guardrails for failures so recovery is predictable, repeatable, and doesn’t deadlock or mask outcomes:

1) Classify errors into “retryable” vs “permanent,” then apply a bounded retry budget.
- Quarantine/retire permanently only for the specific error codes you know cannot succeed until the underlying resource changes.
- For retryable errors, retire after N consecutive failures and reset the counter on any success (so two separate outages don’t accumulate).

2) Validate recovery inputs to prevent “false live” state or unexpected argument errors.
- When using OS/process semantics (pid, signals, locks), ensure the value is in the runtime-accepted range; otherwise treat it as “unknown/missing” so recovery can proceed.

3) Never let cleanup/recovery throw in a way that overwrites the primary outcome.
- If an earlier try/catch already captured the real result, run cleanup as best-effort and preserve the original status/receipt.
- If a later stage might skip worker logic, make sure cleanup still happens on the skip path when needed to keep resumed runs correct.

4) Ensure prerequisites are materialized before running dependent steps.
- If a script/job assumes files exist under a path, either materialize them from the validated runtime source or stage them from where the fixture/runtime actually provides them—avoid unconditional steps that can fail with ENOENT.

Example (retry budget + reset + permanent quarantine):
```ts
const PERMANENT_OPEN_CODES = new Set([
  "EACCES","EPERM","EISDIR","ELOOP","ENAMETOOLONG","ENOTDIR",
]);
const MAX_SESSION_OPEN_ATTEMPTS = 5;

async function readSessionUsage({ session, open, path }) {
  try {
    const file = await open(path, "r");
    session.openFailures = 0; // reset on any success
    // ...read usage...
  } catch (err: any) {
    if (PERMANENT_OPEN_CODES.has(err?.code)) {
      quarantineSession(session);
      return; // or return null, depending on API
    }

    session.openFailures = (session.openFailures ?? 0) + 1;
    if (session.openFailures >= MAX_SESSION_OPEN_ATTEMPTS) {
      quarantineSession(session);
    }
    throw err;
  }
}
```

Use these rules consistently across scanning, lock recovery, resume flows, and filesystem staging so failures degrade gracefully, don’t mask the true outcome, and don’t repeatedly re-trigger the same bad state.