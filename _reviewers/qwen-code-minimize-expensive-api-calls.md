---
title: Minimize expensive API calls
description: When your code depends on GitHub (or other remote) APIs, pagination and
  per-item mutations are often the dominant performance cost. Structure workflows/scripts
  to avoid redundant full scans and to prevent N+1 API patterns unless the workload
  is provably small.
repository: QwenLM/qwen-code
label: Performance Optimization
language: Yaml
comments_count: 3
repository_stars: 26407
---

When your code depends on GitHub (or other remote) APIs, pagination and per-item mutations are often the dominant performance cost. Structure workflows/scripts to avoid redundant full scans and to prevent N+1 API patterns unless the workload is provably small.

Apply this standard:
- **Eliminate repeated scans:** If one step already locates a marker comment (or any ID), pass the ID to later steps via step outputs instead of re-running `gh api --paginate`.
- **Reduce fan-out:** If you find a loop that triggers one API mutation per matched item (N calls for N matches), prefer batching/chunking when match counts can be large.
- **If you keep per-item calls, justify it:** Ensure expected match volume (or other constraints) makes the overhead negligible, and document the reasoning.

Example pattern (avoid re-paginating; pass `comment_id` forward):
```yaml
- name: Post status comment
  id: post_status
  if: ${{ always() }}
  run: |
    set -euo pipefail
    MARKER='<!-- autofix-status -->'
    # Locate or create status comment, then output its id
    STATUS_ID=$(gh api "repos/${REPO}/issues/${PR}/comments" --paginate \
      | jq -rs --arg m "$MARKER" --arg ab "$AUTOFIX_BOT" \
        '[.[][] | select((.user.login // "") == $ab) | select((.body // "") | contains($m))] | last | .id // empty')
    if [[ -z "$STATUS_ID" ]]; then
      STATUS_ID=$(gh api "repos/${REPO}/issues/${PR}/comments" -f body="..." --jq '.id')
    else
      gh api --method PATCH "repos/${REPO}/issues/comments/${STATUS_ID}" -f body="..." >/dev/null
    fi
    echo "comment_id=$STATUS_ID" >> "$GITHUB_OUTPUT"

- name: Finalize
  if: ${{ always() }}
  run: |
    set -euo pipefail
    STATUS_ID='${{ steps.post_status.outputs.comment_id }}'
    # Use STATUS_ID directly; do NOT re-run --paginate here.
    echo "Using status comment id: $STATUS_ID"
```

This reduces execution time, API usage, and flakiness from rate limits—especially across repeated rounds or high-comment PRs.