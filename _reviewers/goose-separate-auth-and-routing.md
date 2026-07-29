---
title: Separate auth and routing
description: 'When using OpenAI-compatible providers/proxies, treat authentication
  and endpoint routing as separate concerns:

  - **Auth comes only from the API key** (e.g., `OPENAI_API_KEY`). If the key is missing/unloaded,
  requests may be sent with no auth and you’ll typically see `401` (e.g., `No api
  key passed in`).'
repository: aaif-goose/goose
label: Security
language: Markdown
comments_count: 1
repository_stars: 51876
---

When using OpenAI-compatible providers/proxies, treat authentication and endpoint routing as separate concerns:
- **Auth comes only from the API key** (e.g., `OPENAI_API_KEY`). If the key is missing/unloaded, requests may be sent with no auth and you’ll typically see `401` (e.g., `No api key passed in`).
- **Routing comes from host/path settings** (e.g., `OPENAI_HOST` as the proxy root *without* a trailing path, and `OPENAI_BASE_PATH` as the served route such as `v1/chat/completions`). If the path is wrong, you’ll typically see `404` for the expected operation/route.
- **Don’t mix configuration approaches**—choose one documented method for selecting the proxy.

Example (proxy via OpenAI-compatible settings):
```bash
# Proxy root only (no trailing path)
export OPENAI_HOST="https://your-proxy.example.com"

# Path the proxy serves (ensure it matches, e.g., v1/chat/completions)
export OPENAI_BASE_PATH="/v1/chat/completions"

# Auth token used by the client
export OPENAI_API_KEY="$YOUR_KEY"
```

Practical troubleshooting:
- If you get **401** with “No api key passed in” → check that `OPENAI_API_KEY` is set and loaded.
- If you get **404** for `chat/completions` → fix `OPENAI_BASE_PATH` (and verify it matches what the proxy actually exposes).