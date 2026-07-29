---
title: Validate model limits
description: 'When integrating LLM providers, don’t assume the provider’s model spec
  equals what the specific API endpoint will actually accept. Enforce two checks in
  your model configuration: (1) set `context_limit` to a safe upper bound that matches
  the endpoint’s effective cap, and (2) restrict model selection to a curated allowlist
  of chat-capable models instead of...'
repository: aaif-goose/goose
label: AI
language: Json
comments_count: 2
repository_stars: 51876
---

When integrating LLM providers, don’t assume the provider’s model spec equals what the specific API endpoint will actually accept. Enforce two checks in your model configuration: (1) set `context_limit` to a safe upper bound that matches the endpoint’s effective cap, and (2) restrict model selection to a curated allowlist of chat-capable models instead of auto-loading the full `/v1/models` catalog (which can include unsupported modalities).

Practical application:
- For each provider/model entry, verify the *endpoint-enforced* context cap (not just vendor docs/specs). If there’s evidence the endpoint rejects above (e.g., 200k vs. 1M), set `context_limit` accordingly or keep a conservative cap until confirmed otherwise.
- For OpenAI-compatible gateways, set `dynamic_models` to `false` and maintain an explicit list of supported chat models.

Example (pattern):
```json
{
  "api_key_env": "PROVIDER_API_KEY",
  "base_url": "https://api.provider.com/v1/chat/completions",
  "dynamic_models": false,
  "models": [
    { "name": "Chat-Model-A", "context_limit": 200000 },
    { "name": "Chat-Model-B", "context_limit": 64000 }
  ]
}
```