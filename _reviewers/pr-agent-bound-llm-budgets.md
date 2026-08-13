---
title: Bound LLM Budgets
description: When configuring generative AI for code-review workflows, keep prompts
  and model behaviors tightly bounded to control latency/cost while preserving quality.
repository: the-pr-agent/pr-agent
label: AI
language: Toml
comments_count: 4
repository_stars: 12523
---

When configuring generative AI for code-review workflows, keep prompts and model behaviors tightly bounded to control latency/cost while preserving quality.

Apply these rules:
1) Constrain prompt instructions and outputs
- Avoid overly verbose “blanket” instructions.
- Use explicit, small output targets (e.g., word limits).

Example (prompt constraint):
```toml
# Prefer a short, bounded requirement for summaries
todo_summary: str = Field(
  description="Up to 6 words summarizing the functional areas of TODO comments found in the code. Return 'No' if none."
)
```

2) Cap extended thinking / generation budgets
- Don’t set large token budgets by default; cap them to prevent linear time growth.
- Keep both input budget and max output token caps conservative (e.g., 2048 as a practical default).

Example (token caps):
```toml
enable_claude_extended_thinking = false
extended_thinking_budget_tokens = 2048
extended_thinking_max_output_tokens = 2048
```

3) Make weaker/cost-saving model usage opt-in
- Only use `model_weak` (or similar) if the user explicitly defines it; otherwise prioritize quality.

4) Choose fallbacks that can actually handle expected context
- Use fallback models only if they meet context-length requirements; avoid fallbacks known to degrade the experience (e.g., too-small context for PRs).

This standard reduces runaway costs/latency, improves consistency of LLM outputs, and prevents poor review quality caused by unsuitable model/fallback choices.