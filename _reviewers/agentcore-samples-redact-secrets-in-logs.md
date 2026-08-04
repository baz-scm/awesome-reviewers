---
title: Redact Secrets in Logs
description: 'When adding logging/debug output for authentication/authorization, apply
  two rules:


  1) Auth configuration metadata is OK

  - Safe to print non-sensitive authorization configuration (e.g., allowed OAuth flows,
  explicit auth flows, client name) since it does not expose credentials.'
repository: awslabs/agentcore-samples
label: Security
language: Python
comments_count: 4
repository_stars: 3244
---

When adding logging/debug output for authentication/authorization, apply two rules:

1) Auth configuration metadata is OK
- Safe to print non-sensitive authorization configuration (e.g., allowed OAuth flows, explicit auth flows, client name) since it does not expose credentials.

2) Any secret-like value must be redacted/truncated
- Never log full API keys, access tokens, gateway tokens, or other credentials.
- If logging is necessary for troubleshooting, log only a masked/truncated representation using a consistent scheme (e.g., mask most characters and optionally show only the last 8 chars).

Example (safe logging pattern):
```python

def mask_secret(value: str, keep_last: int = 8) -> str:
    if not value:
        return '***'
    return f"{'*' * 20}...{value[-keep_last:] if len(value) > keep_last else '***'}"

# Usage
logging.info(f"   ANTHROPIC_API_KEY: {mask_secret(anthropic_api_key) if anthropic_api_key else '***'}")
logging.info(f"   GATEWAY_ACCESS_TOKEN: {mask_secret(gateway_access_token) if gateway_access_token else '***'}")

# Auth configuration metadata is fine (no tokens/keys)
logging.info(f"   AllowedOAuthFlows: {client.get('AllowedOAuthFlows', [])}")
logging.info(f"   ExplicitAuthFlows: {client.get('ExplicitAuthFlows', [])}")
```

Enforcement guidance:
- Any change that increases the amount of secret data printed (or prints raw tokens/keys) should be rejected.
- Any change that makes masking less reliable should be rejected; preserve the existing approved truncation/redaction behavior.