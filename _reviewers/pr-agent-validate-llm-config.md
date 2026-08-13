---
title: Validate LLM Config
description: Ensure any LLM configuration is provider/model compatible by (1) validating
  cross-parameter constraints (especially token budget vs max output) and (2) applying
  only parameters supported by that specific provider/model (e.g., don’t set `temperature`
  for configs that don’t allow it). This prevents runtime BadRequest errors and reduces
  wasted latency/cost.
repository: the-pr-agent/pr-agent
label: AI
language: Markdown
comments_count: 2
repository_stars: 12523
---

Ensure any LLM configuration is provider/model compatible by (1) validating cross-parameter constraints (especially token budget vs max output) and (2) applying only parameters supported by that specific provider/model (e.g., don’t set `temperature` for configs that don’t allow it). This prevents runtime BadRequest errors and reduces wasted latency/cost.

Apply this standard:
- Add config validation on startup/PR-time:
  - Fail fast when numeric constraints are violated (e.g., max output must be greater than the thinking budget).
  - Cap or sanity-check overly large budgets to avoid extreme latency/cost.
- Gate unsupported parameters:
  - Only set `temperature` (or other unsupported fields) when the target provider/model supports them.

Example (token constraint + conditional parameter):
```toml
[config]
# Extended thinking (example shape)
enable_claude_extended_thinking = false
extended_thinking_budget_tokens = 2048
extended_thinking_max_output_tokens = 4096 # must be > budget
```

```python
def build_generation_kwargs(model_id: str, cfg: dict):
    kwargs = {}

    # Only include temperature when supported by the selected config/provider.
    if cfg.get("provider") == "bedrock" and "claude-3" in model_id:
        if cfg.get("temperature") is not None:
            kwargs["temperature"] = cfg["temperature"]

    # Validate extended-thinking constraint if enabled.
    if cfg.get("enable_claude_extended_thinking"):
        budget = cfg["extended_thinking_budget_tokens"]
        max_out = cfg["extended_thinking_max_output_tokens"]
        if max_out <= budget:
            raise ValueError("extended_thinking_max_output_tokens must be greater than extended_thinking_budget_tokens")

    return kwargs
```

Keep a small compatibility matrix (provider/model → supported params + constraints) and add a couple of unit tests that assert known invalid combinations are rejected before hitting the inference API.