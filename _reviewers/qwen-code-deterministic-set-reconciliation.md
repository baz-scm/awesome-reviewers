---
title: Deterministic Set Reconciliation
description: 'When you correlate agent outputs, commit history, or prior workflow
  state across time, avoid fuzzy matching and “best-effort” heuristics. Instead:

  1) Associate via stable identifiers (IDs), not text substrings.'
repository: QwenLM/qwen-code
label: Algorithms
language: Yaml
comments_count: 5
repository_stars: 26407
---

When you correlate agent outputs, commit history, or prior workflow state across time, avoid fuzzy matching and “best-effort” heuristics. Instead:
1) Associate via stable identifiers (IDs), not text substrings.
2) Treat reviewer/record collections as sets and reconcile them with drift awareness (manually dismissed items must be excluded even if they never reviewed).
3) Persist the right state invariant for future runs—don’t overwrite marker state with post-drift values that erase manual decisions.
4) Use precise selectors for markers/reports (e.g., `startswith(marker)` and a dedicated “substantive report” marker), not “newest non-running”.

Example (stable association + precise marker selection):
```bash
# Commit message should include fix.id (written by the agent)
# Then drop matching becomes exact.
# e.g., msg contains(fix.id) rather than 30-char substring.
node -e '...
  const droppedMsgs = process.env.DROPPED_MSGS.split("\n");
  f.fixes = f.fixes.filter(fix => !droppedMsgs.some(msg => msg.includes(fix.id)));
'
```

Example (drift-aware desired-set update):
```bash
# prev_desired = what you previously intended *before* drift
# current = actually requested now
# reviewed = who already submitted a review
# Exclude manual dismissals: reviewers in prev_desired but not in current and not in reviewed.
drift=$(jq -cn --argjson p "$prev_desired" --argjson c "$current" --argjson r "$reviewed" '$p - $c - $r')
desired=$(jq -cn --argjson d "$desired" --argjson drift "$drift" '$d - $drift | sort')
# IMPORTANT: write marker using pre-drift desired, not the post-drift one.
marker_body="${marker} {\"desired\":$pre_drift_desired} -->"
```

Operational rule: if a matching/reconciliation step can plausibly pick the wrong entity due to wording, ordering, or manual UI actions, treat that as an algorithmic correctness failure—tighten inputs (IDs/markers), and tighten set logic (invariants + drift).