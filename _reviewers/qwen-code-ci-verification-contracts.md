---
title: CI Verification Contracts
description: 'CI/CD verification steps must produce *truthful, reproducible, human-visible*
  evidence under hard environment constraints (time, filesystem, available tools,
  git history). Concretely:'
repository: QwenLM/qwen-code
label: CI/CD
language: Markdown
comments_count: 6
repository_stars: 26407
---

CI/CD verification steps must produce *truthful, reproducible, human-visible* evidence under hard environment constraints (time, filesystem, available tools, git history). Concretely:

1) **Keep evidence visible across stages**
- If a verification fails and you mark a finding `status: "dropped"`, ensure it still appears in the human-facing report stream (not just an internal `fixes` list). Align `.fixes`/`.reportOnly` semantics so “dropped because verification failed” is still auditable.

2) **Make verification rerunnable (idempotent cleanup)**
- Any scratch directories/worktrees created by the verifier must be either:
  - created with names matching the workflow cleanup glob, or
  - explicitly removed by the skill itself.

Example (safe worktree lifecycle):
```sh
# use a directory name that matches cleanup patterns (or remove explicitly)
git worktree add tmp/base-verify-tree HEAD^1
# ... run A/B ...
# always remove what you registered
git worktree remove --force tmp/base-verify-tree
```

3) **Don’t promise evidence you can’t obtain**
- If the CI checkout depth/history cannot support a requirement (e.g., per-commit attribution), detect reachability first and then:
  - verify only what is available, and
  - record the missing part as *Not covered* rather than fabricating tables.

4) **Run only gates your container can actually run; avoid mutating the PR tree**
- Before claiming lint/tests “passed”, ensure required pinned binaries are present.
- Prefer setup-only install steps, then run *non-mutating* checks. For example, if setup installs formatters/linters:
```sh
node scripts/lint.js --setup
# then only non-mutating checks (examples)
node scripts/lint.js --actionlint
# never call the mutating no-arg form that rewrites the PR tree
```
- If a tool cannot be installed in the verify container within budget, explicitly report “not run”.

5) **Validate controls don’t accidentally execute head code**
- In monorepos, symlinks or internal workspace resolution can cause a “base” run to load changed head code. Before trusting an A/B control, confirm the resolved realpaths of internal dependencies point to the intended base checkout.

6) **Follow-up reports must snapshot the newest substantive evidence**
- For subsequent `/verify` rounds, snapshot the latest *substantive* previous report (not transient “running/weak” marker comments) so prior unresolved findings aren’t erased.

Applying these rules prevents CI/CD from silently hiding failures, failing reruns due to stale artifacts, overstating verification certainty, or producing non-comparable A/B results—raising reliability of automated gates and maintainer trust in the evidence.