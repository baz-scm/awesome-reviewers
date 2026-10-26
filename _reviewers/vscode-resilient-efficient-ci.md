---
title: Resilient Efficient CI
description: 'CI/CD workflows should be resilient, deterministic, and efficient:


  1) Required checks should be resilient and scope-correct

  - Use a single “PR gate” (or equivalent) that passes when all relevant test jobs
  succeeded or were skipped.'
repository: microsoft/VSCode
label: CI/CD
language: Yaml
comments_count: 7
repository_stars: 194303
---

CI/CD workflows should be resilient, deterministic, and efficient:

1) Required checks should be resilient and scope-correct
- Use a single “PR gate” (or equivalent) that passes when all relevant test jobs succeeded or were skipped.
- Prefer a fails-open approach when upstream planning/change detection is unavailable, so outages don’t block PR merges.
- Use always() so you still report job outcomes when failures happen.

Example (pattern):
```yaml
pr-gate:
  name: PR Gate
  needs: [changes, linux-electron-unit-tests, ...]
  if: ${{ always() }}
  runs-on: ubuntu-24.04
  steps:
    - name: Check job results
      env:
        NEEDS: ${{ toJSON(needs) }}
      run: |
        set -euo pipefail
        detection=$(jq -r '.changes.result' <<< "$NEEDS")
        # If detection/planner failed, do not fail the gate; let PR proceed.
        status=0
        # ...set status based on required job results...
        exit $status
```

2) Optional artifacts/selection inputs must not accidentally expand the test scope
- If a “test plan”/selection artifact might be absent, handle the missing artifact explicitly (e.g., download step continues on error and then remove the plan so tests run with the intended fallback).
- Ensure the behavior is deterministic: missing plan => clearly defined “run all” (or “skip”), but not an accidental mix.

Example (pattern):
```yaml
- name: Download unit test plan
  if: ${{ inputs.unit_tests && inputs.unit_test_selection }}
  continue-on-error: true
  uses: actions/download-artifact@<sha>
  with:
    pattern: unit-test-plan
    path: .build/unit-test-plan

# On download failure, delete the directory so tests see "no plan".
- name: Remove plan if missing
  if: ${{ steps.download.outcome == 'failure' }}
  run: rm -rf .build/unit-test-plan
```

3) Don’t multiply heavy CI preparation for small additional test subsets
- Avoid adding separate jobs/workflows that repeat full repo checkout/build/dependency setup just to run a small extra shard.
- Instead: reuse prepared outputs (artifacts, caches, restore/transpile/Electron setup) or run the additional test subset concurrently on the same prepared runner.
- Only keep isolated jobs when overlap would be unsafe (e.g., tests that mutate shared system/network state).

4) Add retries only to network-dependent steps, with targeted env knobs
- Set retryCountOnTaskFailure on the specific step types that are network/caching dependent.
- For cargo/crate fetching, scope env/network tuning to the crate-fetching steps (e.g., CARGO_NET_RETRY / disable HTTP multiplexing) rather than changing unrelated build/lint behavior.

Example (pattern):
```yaml
- script: cargo build
  retryCountOnTaskFailure: 2
  env:
    CARGO_HTTP_MULTIPLEXING: "false"
    CARGO_NET_RETRY: "5"
```

Adopt this checklist in PR reviews for CI/CD changes to prevent merge-blocking outages, avoid accidental test-scope changes, reduce duplicated CI cost, and improve robustness against transient network failures.