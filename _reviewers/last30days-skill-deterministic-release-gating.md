---
title: Deterministic Release Gating
description: When automating CI/CD releases, make “release vs non-release” and downstream
  publishing deterministic by (1) gating on explicit signals and (2) explicitly triggering
  the next workflow step.
repository: mvanhorn/last30days-skill
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 57799
---

When automating CI/CD releases, make “release vs non-release” and downstream publishing deterministic by (1) gating on explicit signals and (2) explicitly triggering the next workflow step.

Apply these rules:
- Prefer explicit metadata over heuristics: use a required label (e.g., `release`) rather than parsing PR titles to decide exemptions.
- If a later job depends on the release state (e.g., tagging), ensure the gating condition is also satisfied for the merged PR (label present on the PR you merged).
- Don’t rely on implicit workflow triggering from tag pushes for critical publishing. After creating the tag, explicitly invoke the downstream publish/build workflow (e.g., `workflow_dispatch` with `tag=`).

Example pattern (Bash label gating + explicit downstream dispatch):
```bash
LABELS="$(gh api "repos/${GITHUB_REPOSITORY}/issues/$PR_NUMBER/labels" --jq '.[].name')"
IS_RELEASE=0
if printf '%s\n' "$LABELS" | grep -qx 'release'; then
  IS_RELEASE=1
fi

# ... later after creating/pushing tag ...
# Trigger publish workflow deterministically
gh workflow run release.yml -f tag="${TAG}" --ref "${DEFAULT_BRANCH}" 
```

This reduces accidental bypasses and makes release pipelines predictable and auditable.