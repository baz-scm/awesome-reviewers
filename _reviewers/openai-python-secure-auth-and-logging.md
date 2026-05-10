---
title: Secure Auth and Logging
description: Security-sensitive code must ensure (1) the correct auth path is used
  without accidental overrides, (2) sensitive auth material is never leaked in logs,
  and (3) auth-mode “sentinels” and provider handles can’t be accidentally triggered
  or misused.
repository: openai/openai-python
label: Security
language: Python
comments_count: 8
repository_stars: 30731
---

Security-sensitive code must ensure (1) the correct auth path is used without accidental overrides, (2) sensitive auth material is never leaked in logs, and (3) auth-mode “sentinels” and provider handles can’t be accidentally triggered or misused.

Apply these rules:
- Auth path discipline: Refresh/call a callable API-key (or bearer token provider) only on the exact fallback path where API-key auth is used; never invoke it for the Azure AD token path. Add regression tests for both sync/async flows.
- Don’t override user headers: When constructing request headers, avoid unconditionally setting `Authorization` if a user may have provided one. If you must set it, gate it behind an explicit “header missing/expected mode” check.
- Avoid fragile sentinels: If you use a sentinel value to trigger a special auth mode, it must be private and non-guessable to prevent collisions (e.g., not a human-typed string).
- Never log secrets: Centralize header redaction (e.g., for `api-key` and `authorization`) and ensure all response/request logging uses it; cover it with unit tests.

Example (redact sensitive headers):
```py
SENSITIVE_HEADERS = {"api-key", "authorization"}

def redact_sensitive_headers(headers: dict[str, str]) -> dict[str, str]:
    return {k: ("<redacted>" if k.lower() in SENSITIVE_HEADERS else v) for k, v in headers.items()}
```

Example (auth provider discipline):
- In your Azure options preparation, only call `_refresh_api_key()` (or refresh a callable provider) when you’re about to use API-key auth (i.e., when AD token auth isn’t active / you’re falling back). Add tests that assert the provider is *not* called when AD auth is used.
