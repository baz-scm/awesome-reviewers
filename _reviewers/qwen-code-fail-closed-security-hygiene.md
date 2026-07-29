---
title: Fail-Closed Security Hygiene
description: 'Security gates and cleanup must be *fail-closed* and *boundary-proven*.


  Apply these rules when implementing/adjusting secure workflows:


  1) **Authorization must not degrade**'
repository: QwenLM/qwen-code
label: Security
language: JavaScript
comments_count: 4
repository_stars: 26407
---

Security gates and cleanup must be *fail-closed* and *boundary-proven*.

Apply these rules when implementing/adjusting secure workflows:

1) **Authorization must not degrade**
- Treat every principal that can spend execution/budget as part of the gate (e.g., both the PR author whose code runs and the commenter who triggers the workflow slot).
- Ensure command routing/case normalization can’t accidentally fall through to weaker paths.
- Regression tests should **execute** the gate and assert the same outcome for differently cased commands.

2) **Re-sweep after PR-controlled lifecycle scripts**
- If the workflow runs `npm ci/build` (or any PR-controlled lifecycle hooks), assume they may plant artifacts into runner temp/upload staging.
- Immediately **before** agent/proxy start (and before uploads), do `rm -rf` then `mkdir -p` in the same step, and keep ordering stable (rm → mkdir → proxy/agent).

3) **Prove the auth boundary with real requests**
- Don’t “test” authorization by asserting proxy configuration/nonce alone.
- Start the real proxy and send HTTP requests:
  - no `Authorization` header → **401**
  - wrong token → **401**
  - correct token → **200**
  - wrong route → **403**

4) **Make security tests hermetic (no global/system config influence)**
- For filesystem/git cleanup/symlink-escape tests, neutralize global/system git settings (e.g., set `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_SYSTEM=/dev/null`).
- Re-run the same exploit scenario with a deliberately planted risky setting (e.g., global `core.hooksPath`) so failures can’t be masked by developer machines.

Example (authorization routing + fail-closed execution):
```bash
# In the shell gate script
body_lc="${COMMENT_BODY,,}"
case "$body_lc" in
  *@qwen-code /verify*)
    # FAIL CLOSED: require BOTH principals to have permission
    # (e.g., should_run=false unless author_has_write && commenter_has_write)
    ;;
  *@qwen-code /tmux*)
    # Keep existing narrower gate
    ;;
  *)
    should_run=false
    ;;
esac
```

Example (post-PR lifecycle hygiene):
```bash
# In the agent step, immediately before upload/agent start
rm -rf "$RUNNER_TEMP/verify-results"
mkdir -p "$RUNNER_TEMP/verify-results"
start_openai_proxy
```