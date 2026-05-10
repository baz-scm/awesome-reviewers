---
title: Deterministic API Contracts
description: 'When designing API client/runner behavior, ensure the contract is explicit,
  state-driven, and aligned with what the server actually supports.


  Apply these rules:'
repository: anthropics/anthropic-sdk-python
label: API
language: Python
comments_count: 4
repository_stars: 3392
---

When designing API client/runner behavior, ensure the contract is explicit, state-driven, and aligned with what the server actually supports.

Apply these rules:
- Prefer explicit client parameters for critical inputs; allow environment-variable defaults, but don’t make env-only the only configuration path.
- For any follow-up request that depends on conversation/session state, derive IDs/containers from the *current in-memory state* (e.g., the last assistant message in the loop), not from prior API responses that may be stale after state mutations.
- Keep schema compilation/transformation limited to features your server and codegen truly support (e.g., treat JSONSchema `enum` as primitives/literals; don’t invent transformations for unsupported composite/object literals).
- Keep the public typed surface minimal: expose only intended methods to type checkers, while still making internal helpers available at runtime when needed.

Example (state-driven follow-up request):
```py
# BAD: reusing container id from a previous API response
# container_id = last_api_response.container.id

# GOOD: use container id from the current last assistant message in state
message = self._get_last_message()
if message.container is not None:
    container_id = message.container.id
    # use container_id for the next tool/assistant step
```

Example (explicit config with env default):
```py
def get_auth_headers(api_key: str | None = None) -> dict[str, str]:
    key = api_key or os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    if not key:
        raise ValueError("Missing api key")
    return {"Authorization": f"Bearer {key}"}
```