---
title: Concise Factual Instructions
description: When writing AI rules or workflow instructions, keep the language concise
  and unambiguous, and for any factual/time-sensitive output require the model to
  derive it from runtime results (never placeholders or estimates). Overusing high-salience
  markers (e.g., many `MANDATORY/CRITICAL` tags) can reduce compliance; instead, make
  requirements explicit via...
repository: awslabs/aidlc-workflows
label: AI
language: Markdown
comments_count: 2
repository_stars: 3849
---

When writing AI rules or workflow instructions, keep the language concise and unambiguous, and for any factual/time-sensitive output require the model to derive it from runtime results (never placeholders or estimates). Overusing high-salience markers (e.g., many `MANDATORY/CRITICAL` tags) can reduce compliance; instead, make requirements explicit via concrete steps.

Application guidelines:
- Prefer clear, short tenets over repeated emphasis keywords.
- For timestamps or other factual fields:
  - Specify the exact format including timezone offset.
  - Explicitly forbid fabricated/estimated values.
  - Require an explicit command to fetch the value, then instruct the model to copy the command output verbatim.

Example (timestamp audit entry):
```bash
# 1) Get real local time in required format
TS=$(date "+%Y-%m-%dT%H:%M:%S%z")
# 2) Use TS exactly as the Timestamp value when appending to audit.md
# e.g., Timestamp: "$TS" (no placeholders like T00:00:00Z)
```
Use the same pattern whenever the rule depends on real-world state (current time, environment values, IDs, outputs), so models across different providers behave consistently.