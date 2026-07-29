---
title: Trusted Error Handling
description: Use strict, non-silent error handling and evidence gating across CI scripts
  and publish steps—especially when untrusted inputs and reruns are involved.
repository: QwenLM/qwen-code
label: Error Handling
language: Yaml
comments_count: 20
repository_stars: 26407
---

Use strict, non-silent error handling and evidence gating across CI scripts and publish steps—especially when untrusted inputs and reruns are involved.

Apply these rules:
1) Never hide failing diagnostics
- Don’t redirect critical command errors to `/dev/null` without capturing them into logs.
- If you must suppress, replace it with a structured warning including the failing command and exit code.

2) Make “no match/empty input” non-fatal under `set -e`
- With `set -euo pipefail`, commands like `grep` can exit 1 when nothing matches; treat that as an expected state (e.g., “empty blocklist”) instead of aborting.

3) Validate output marshalling before downstream parsing
- When writing multi-line or JSON values to `$GITHUB_OUTPUT`, use the multiline-safe `<<EOF` form (heredoc). Never rely on single-line `key=value` for JSON arrays.

4) Treat pipelines as a set of outcomes
- Under `set -e`/`pipefail`, don’t trust only `PIPESTATUS[0]`. Record both producer and consumer stages (e.g., agent + `tee`) and downgrade “pass” to infra error if output writing/truncation failed.

5) Bound all “read/truncate” operations to avoid SIGPIPE under `pipefail`
- When reading verdict/artifacts from potentially large files, cap bytes before `tr|head`/similar pipelines (e.g., `head -c 4096 file | ...`).

6) Gate substantive/terminal publish updates on validated artifacts
- Never overwrite a previous terminal report with a rerun “running” status.
- Don’t add substantive markers or “completed” scope text unless:
  - the run is truly completed, and
  - the required evidence files exist, and
  - artifact download outcome is `success`.
- If artifacts are missing/download failed, publish a weak “results unavailable” message instead of full evidence.

7) Classify infra vs PR failures using trusted signals only
- Avoid grepping PR-controlled stdout/stderr for “ETIMEDOUT/ENOSPC/502” style strings.
- Use non-spoofable signals (runner signal exit codes, timeout budget behavior, kernel OOM lines, or tightly anchored npm reporter prefixes that you can trust).
- If classification is ambiguous, prefer “run incomplete/results unavailable” over incorrectly labeling a PR failure as infra (or vice versa).

Illustrative bash pattern (combine rules 2,4,6):
```bash
set -euo pipefail

# 1) empty-match is expected
BLOCKED_USERS="$(grep -vE '^\s*#' blocklist | ... | sort -u || true)"

# 2) pipeline status: capture both stages
set +e
timeout 25m run_agent | tee output.jsonl
PIPE_STATUS=(${PIPESTATUS[@]})
AGENT_CODE=${PIPE_STATUS[0]}
TEE_CODE=${PIPE_STATUS[1]:-0}
set -e

verdict='pass'
if [ "$AGENT_CODE" -ne 0 ] || [ "$TEE_CODE" -ne 0 ]; then
  verdict='infra-error'
fi

# 3) only publish substantive if report exists
if [ "$verdict" = 'pass' ] && [ -f tmp/verify-*/report.md ]; then
  publish_substantive
else
  publish_weak_results_unavailable
fi
```

Outcome: fewer silent CI failures, correct publish/evidence preservation across reruns, and accurate infra-vs-PR labeling so developers don’t waste time rerunning code when the true problem was infrastructure (or the opposite).