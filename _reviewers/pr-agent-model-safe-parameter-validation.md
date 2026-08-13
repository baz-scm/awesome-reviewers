---
title: Model-Safe Parameter Validation
description: 'Adopt a model/provider-aware configuration standard: before sending
  requests to LLM APIs, validate that every model-specific parameter (reasoning effort,
  thinking features, temperature constraints, system support) is supported for that
  exact model/provider, and apply overrides safely without accidentally changing unrelated
  limits.'
repository: the-pr-agent/pr-agent
label: AI
language: Python
comments_count: 8
repository_stars: 12523
---

Adopt a model/provider-aware configuration standard: before sending requests to LLM APIs, validate that every model-specific parameter (reasoning effort, thinking features, temperature constraints, system support) is supported for that exact model/provider, and apply overrides safely without accidentally changing unrelated limits.

Apply these rules:
1) Validate model capability before passing parameters
- Keep a centralized mapping/list of model capabilities (e.g., supported `reasoning_effort` values; whether `thinking`/extended thinking requires `temperature=1`; whether `system` is ignored or unsupported).
- If a user config is invalid for the selected model, either (a) fall back to a safe default known to be valid for that model, or (b) omit the parameter and let the API default.

2) Distinguish input-token vs output-token limits
- Treat `max_tokens` passed to LiteLLM/OpenAI-style APIs as OUTPUT-only, and use the correct separate config for INPUT limits.
- Ensure your token budgeting logic matches what the downstream API expects.

3) When overriding, cap instead of overwriting
- If your code sets an output cap (e.g., provider-specific `max_tokens`), do not overwrite an already-computed/earlier value; cap it (min(existing, override)) so other logic remains intact.

4) Use real token measurement—avoid heuristic clipping
- If you must clip context, prefer encoding-based measurement (or the library’s token estimator). Avoid magic ratios like “2.5 tokens per word”, which can over/under-clip.

5) Don’t introduce model/provider IDs without authoritative references
- For provider-specific model/profile identifiers (e.g., Bedrock inference profiles), only add entries that are verified against official docs; otherwise your token caps or routing can silently misbehave.

Example pattern (safe reasoning_effort + capability validation):
```python
supported = {
  # model_prefix: allowed_values (or None to omit)
  "gpt-5": {"minimal","low","medium","high"},
  "gpt-5.1": {"none","low","medium","high"},
  "gpt-5.2": {"none","minimal","low","medium","high","xhigh"},
}

def choose_reasoning_effort(model: str, requested: str | None) -> str | None:
    # pick the best match (implementation depends on your naming scheme)
    allowed = None
    for prefix, vals in supported.items():
        if model.startswith(prefix):
            allowed = vals
            break
    if not allowed:
        return requested  # or None (omit) if you don’t know

    if requested in allowed:
        return requested
    return "medium"  # or omit parameter so API defaults apply
```

Once this standard is in place, you’ll prevent common production failures: API errors from unsupported parameter combinations, truncated outputs from incorrect token caps, and accidental behavior changes from overwritten limits.