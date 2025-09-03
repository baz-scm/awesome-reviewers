---
title: configurable security settings
description: Security configurations should be made configurable through environment
  variables or runtime settings rather than hardcoded in the application logic. This
  allows teams to adapt security measures to different deployment environments and
  regulatory requirements without code changes.
repository: BerriAI/litellm
label: Security
language: Python
comments_count: 2
repository_stars: 28310
---

Security configurations should be made configurable through environment variables or runtime settings rather than hardcoded in the application logic. This allows teams to adapt security measures to different deployment environments and regulatory requirements without code changes.

Hardcoded security settings create inflexibility and force unnecessary security overhead in environments where it's not needed. Instead, implement conditional security logic that can be toggled based on configuration.

Example of configurable security headers:
```python
@app.middleware("http")
async def add_headers(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    # Make security headers configurable via environment variables
    if os.getenv("ENABLE_SECURITY_HEADERS", "false").lower() == "true":
        response.headers["Content-Security-Policy"] = "default-src 'none'"
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    
    # Conditional validation based on environment requirements
    if os.getenv("STRICT_USER_VALIDATION", "false").lower() == "true":
        if "user_id" in metadata and not _valid_user_id(metadata["user_id"]):
            # Skip invalid user_id rather than failing
            pass
```

This approach enables compliance with regulatory standards when needed while maintaining flexibility for different deployment scenarios.