---
title: Warn on silent failures
description: In automation scripts/workflows, never fail or skip important work silently.
  If a condition decides to omit a capability/flag, or if a command fails with diagnostics
  discarded or a sentinel fallback is used, emit an explicit warning (or notice) that
  includes the relevant inputs and captured error output.
repository: QwenLM/qwen-code
label: Logging
language: Yaml
comments_count: 3
repository_stars: 26407
---

In automation scripts/workflows, never fail or skip important work silently. If a condition decides to omit a capability/flag, or if a command fails with diagnostics discarded or a sentinel fallback is used, emit an explicit warning (or notice) that includes the relevant inputs and captured error output.

Apply this especially to:
- Conditional “omit” paths (e.g., only attach `--notes-start-tag` when an ancestor check passes).
- Command failures where you currently use `2>/dev/null` (capture stderr and log it).
- Ownership/permission-related fallbacks (e.g., UID/GID computed via `stat` falling back to `0`), which should always log computed values or the failure.

Example patterns:

```bash
# 1) Conditional skip with warning
if [[ -n "$PREVIOUS_RELEASE_TAG" ]] && git merge-base --is-ancestor "$PREVIOUS_RELEASE_TAG" HEAD; then
  NOTES_START_TAG_FLAG+=(--notes-start-tag "$PREVIOUS_RELEASE_TAG")
elif [[ -n "$PREVIOUS_RELEASE_TAG" ]]; then
  echo "::warning::PREVIOUS_RELEASE_TAG ($PREVIOUS_RELEASE_TAG) is not an ancestor of HEAD; omitting --notes-start-tag"
fi

# 2) Don’t discard stderr; surface it
result="$(gh api graphql -f query="mutation { minimizeComment(input: {subjectId: \"${node_id}\", classifier: OFF_TOPIC}) { minimizedComment { isMinimized } } }" \
  --jq '.data.minimizeComment.minimizedComment.isMinimized' 2>&1)" || true
if [[ "$result" != "true" ]]; then
  echo "::warning::Failed to minimize ${node_id}: ${result}"
fi

# 3) Log computed/fallback values
RUNNER_UID="$(stat -c '%u' "$RUNNER_TEMP" 2>/dev/null || stat -f '%u' "$RUNNER_TEMP" 2>/dev/null || echo 0)"
RUNNER_GID="$(stat -c '%g' "$RUNNER_TEMP" 2>/dev/null || stat -f '%g' "$RUNNER_TEMP" 2>/dev/null || echo 0)"
echo "Ownership restoration: RUNNER_UID=$RUNNER_UID, RUNNER_GID=$RUNNER_GID"
```

Outcome: operators/oncall can immediately tell whether a path was intentionally skipped, what input caused it, and what underlying command error occurred—reducing 3AM guesswork.