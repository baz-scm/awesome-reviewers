---
title: API Call Correctness
description: 'When automating GitHub (or similar) APIs from CI/workflows, treat API
  access like production client code: make it correct, complete, and safely reconcilable.'
repository: QwenLM/qwen-code
label: API
language: Yaml
comments_count: 4
repository_stars: 26407
---

When automating GitHub (or similar) APIs from CI/workflows, treat API access like production client code: make it correct, complete, and safely reconcilable.

**Standards**
1) **Use the approved API client/tooling**
   - Prefer `gh api` (or your org’s standard client) over raw `curl` to avoid missing auth headers, API version headers, and content negotiation.

2) **Never assume list endpoints fit in one page**
   - For any endpoint that can grow (reviews, comments, files over time, etc.), use pagination support (e.g., `gh api --paginate ... --jq ...`).

3) **Ensure query filters match the user-facing intent**
   - If an input claims a time window (e.g., `hours`), the GraphQL/REST query must apply that window to *all* relevant connections, or explicitly document the asymmetry.

4) **Reconcile managed state only where provenance is knowable**
   - If the API cannot tell whether an item was created by your workflow vs. by external sources (e.g., CODEOWNERS), avoid destructive “DELETE everything not in desired” logic.
   - Instead, reconcile only the subset you can prove you own (e.g., store a marker, track prior workflow `desired`, or intersect with last workflow-managed set).

**Example pattern**
```sh
set -euo pipefail

# 1) Prefer gh api over curl
# gh api "repos/$GITHUB_REPOSITORY/releases/tags/$RELEASE_TAG" > release.json

# 2) Paginate list results
reviewed_users="$(gh api --paginate "repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}/reviews?per_page=100" \
  --jq '[.[].user.login]')"

# 3) Apply filters that match inputs (conceptual)
# Ensure both issues and PRs use since/updatedAt bounds when hours is provided.

# 4) Safe reconciliation (conceptual)
# Only remove reviewers that were previously added by *this* workflow run.
# managed="$(...)"  # compute current requested_reviewers
# owned="$(...)"    # reviewers your workflow previously managed (tracked/provable)
# desired_owned="$(...)" # desired within owned set
# new_managed = (managed - owned) + desired_owned
```

Applying these rules prevents silent coverage gaps, incorrect reconciliation churn, and maintenance drift in authentication/versioning across API calls.