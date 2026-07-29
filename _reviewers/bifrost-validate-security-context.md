---
title: Validate security context
description: 'Define and enforce security-context behavior as a clear contract, then
  implement CI/runtime logic to match it without brittle assumptions.


  Apply this in two places:'
repository: maximhq/bifrost
label: Security
language: Shell
comments_count: 5
repository_stars: 6862
---

Define and enforce security-context behavior as a clear contract, then implement CI/runtime logic to match it without brittle assumptions.

Apply this in two places:

1) Helm/manifest security-context checks (CI)
- Assert the contract (e.g., “default render does not pin `runAsUser`”), not a magic UID number.
- Prevent substring false positives by using anchored match patterns.
- Scope checks to the exact template(s) whose output you intend to validate, and repeat the same assertions for every render mode (sqlite/deployment/postgres/etc.).

Example pattern:
```sh
# contract: default render must not set runAsUser
helm template bifrost ./helm-charts/bifrost \
  --set image.tag=v1.0.0 \
  > /tmp/out.yaml

if grep -Eq '^[[:space:]]+runAsUser:[[:space:]]*' /tmp/out.yaml; then
  echo "Fail: runAsUser must not be pinned in default render"
  exit 1
fi
```

2) Startup permissions (runtime)
- Don’t assume the container has privilege to `chown`/fix ownership (avoid CAP_CHOWN-dependent correctness).
- Use an actual writability probe for the target data dir, create it when possible, and if it’s not writable, fail early with actionable, platform-aware guidance.
- Avoid advising securityContext values that may be rejected by the target platform’s admission controller (e.g., OpenShift `fsGroup` constraints).

Net effect: fewer admission/runtime surprises and fewer CI “green but wrong” security-context failures.