---
title: Security Invariants Testing
description: 'Treat CI/workflow security like production security code: define explicit
  invariants, enforce them defensively, and lock them with executable regression tests—especially
  in workflows that run in privileged contexts (e.g., pull_request_target) or execute
  untrusted PR code.'
repository: QwenLM/qwen-code
label: Security
language: Yaml
comments_count: 14
repository_stars: 26407
---

Treat CI/workflow security like production security code: define explicit invariants, enforce them defensively, and lock them with executable regression tests—especially in workflows that run in privileged contexts (e.g., pull_request_target) or execute untrusted PR code.

Apply these rules:
1) Pin third-party actions by immutable SHA
- Never use mutable tags (e.g., actions/cache@v4) in privileged contexts.
- Require the same “40-char SHA pin” convention for all actions.

2) Fail-closed authorization and principal resolution
- Gate execution on the correct identity (e.g., PR author if that’s the executed code path).
- Reject on missing principal, missing/empty permissions, 404s, or any API failure.
- If a run waits in a queue, re-check permissions immediately before executing.
- Pin the authorized head OID and refuse to run if checkout HEAD differs.

3) Credential minimization and strict scoping
- Keep tokens out of environments where untrusted code runs.
- Use step-level env only for the steps that need them.
- For pull_request_target checkouts: use persist-credentials: false.

4) Prevent control/data-plane poisoning
- Never select “previous report” or “running status” purely by prose/substring; use dedicated machine markers.
- For agent-produced reports: validate structured inputs (e.g., totals consistency) and HTML-escape untrusted content.
- Add executable tests for escaping and truncation behavior.

5) Filesystem hardening for self-hosted/persistent workspaces
- Assume symlinks and prior run state can be adversarial.
- Use symlink-safe deletion (unlink entries without following) and canonicalize any delete targets to remain inside the workspace.
- Ensure cleanup happens both before and after untrusted execution, with regression tests that fail when safety guards are removed.

6) Add/extend executable regression tests for invariants
- If a security invariant exists (repo guard, persist-credentials, cache restore-only, marker usage, escaping implementation, symlink-safe cleanup, re-auth/head pinning), it must be asserted by an automated workflow test.

Minimal examples (adapt patterns):

Action pinning:
```yaml
- uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
- uses: actions/cache/restore@0057852bfaa89a56745cba8c7296529d2fc39830 # v4.x.y pinned
```

Avoid embedding step outputs directly into shell:
```yaml
- name: Record receipt
  env:
    POOL_RUN_ID: '${{ steps.dispatch.outputs.run_id }}'
  run: |
    printf '%s\n' "Pool run: $POOL_RUN_ID" >> "$GITHUB_STEP_SUMMARY"
```

Fail-closed principal handling (pattern):
```bash
# deny on missing/empty principal or permission API failures
if [ -z "$PR_AUTHOR" ] || ! permission="$permission_api_result"; then
  echo "decision=skip" >> "$GITHUB_OUTPUT"
  exit 0
fi
case "$permission" in
  admin|maintain|write) : ;;
  *) echo "decision=skip" >> "$GITHUB_OUTPUT"; exit 0 ;;
esac
```

Run the above as a checklist for every security-critical workflow change: if you can’t test the invariant, you don’t truly have one.