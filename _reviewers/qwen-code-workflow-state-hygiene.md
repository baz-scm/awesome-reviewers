---
title: Workflow State Hygiene
description: 'CI/CD workflows should enforce *state invariants* across steps, runs,
  and runners: later steps must only execute when earlier phases truly produced a
  valid outcome, and all per-run state must be cleaned/flushed and permission-safe—especially
  on persistent self-hosted runners.'
repository: QwenLM/qwen-code
label: CI/CD
language: Yaml
comments_count: 11
repository_stars: 26407
---

CI/CD workflows should enforce *state invariants* across steps, runs, and runners: later steps must only execute when earlier phases truly produced a valid outcome, and all per-run state must be cleaned/flushed and permission-safe—especially on persistent self-hosted runners.

Apply these rules:

1) Gate downstream steps on all relevant phase outputs
- If you have `gate -> verify -> push`, the push step’s `if:` must include *both* gate success and verify’s final result (e.g., not `no-fixes`).

```yaml
# good: push requires gate=fixed AND verify != no-fixes
- name: Push and open PR
  if: ${{ steps.gate.outputs.result == 'fixes' && steps.verify.outputs.result != 'no-fixes' }}
```

2) Keep published artifacts consistent after reverts/aborts
- If `verify` reverts commits, update the same data files/records you uploaded earlier (e.g., `findings.json`) so downstream consumers never see stale statuses.

3) Flush per-run temp/state on persistent runners
- Before creating directories used by the run, remove old content from the previous run.

```bash
rm -rf "$RUNNER_TEMP/verify-results" "$RUNNER_TEMP/verify-context" 2>/dev/null || true
mkdir -p "$RUNNER_TEMP/verify-results" "$RUNNER_TEMP/verify-context"
```

4) Restore both ownership *and write permissions* after hardening
- Re-`chown` without re-`chmod` can still break later cleanups/checkouts (EACCES). Restore mode to allow deletes/unlinks.

```bash
chown -R "$RUNNER_UID:$RUNNER_GID" "$GITHUB_WORKSPACE" || true
chmod -R u+rwX "$GITHUB_WORKSPACE" || true
```

5) Make workflow behavior robust to cache misses and checkout edge-cases
- Ensure directories exist before `chown` when caches may miss.
- Use correct sparse-checkout settings (and path filters) so checkout doesn’t fail and the router doesn’t override reviewer intent on non-target file changes.

6) Prevent CI/resource hangs with explicit bounds
- Any job that only downloads/upload/post should have a small `timeout-minutes`.
- Add tests/guardrails for cancellation/pending states so PR identifiers don’t become empty.

7) Keep concurrency predicates exact
- Ensure that `concurrency.group` logic matches the job’s runnable triggers; otherwise one command (e.g., `/verify`) can displace another (e.g., `/triage`).

If your workflow cannot be proven under: (a) cancellations, (b) persistent runner reuse, (c) cache misses, and (d) permission/mode changes, it’s a CI reliability issue—fix it with the invariants above before merging.