---
title: Configurable security with defaults
description: Make security features configurable through environment variables or
  configuration files, but always implement secure defaults. This allows teams to
  adapt security controls to their specific deployment environments while maintaining
  a secure baseline.
repository: kubeflow/kubeflow
label: Security
language: Python
comments_count: 1
repository_stars: 15064
---

Make security features configurable through environment variables or configuration files, but always implement secure defaults. This allows teams to adapt security controls to their specific deployment environments while maintaining a secure baseline.

When implementing configurable security features:
1. Use secure default values that prioritize security (e.g., "Strict" for SameSite cookies)
2. Validate input configurations and fallback to secure defaults when invalid
3. Document all security configurations and their implications

Example from CSRF implementation:
```python
# Read SameSite configuration from environment with secure default
samesite = os.environ.get("CSRF_SAMESITE", "Strict")

# Validate the input to ensure only secure options are accepted
if samesite not in ["Strict", "Lax", "None"]:
    samesite = "Strict"  # Fallback to secure default

# Apply the configuration to the cookie
response.set_cookie(
    "CSRF_COOKIE", 
    csrf_token,
    httponly=True,
    secure=True,
    samesite=samesite
)
```

Document this configuration in your README:
```markdown
## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| CSRF_SAMESITE | SameSite attribute for CSRF cookies (Strict, Lax, None) | Strict |
```

This approach balances security with flexibility, allowing secure operation in various environments while maintaining strong defaults.
