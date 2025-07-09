---
title: Sanitize debug output
description: Never print or log sensitive information such as tokens, passwords, or
  secrets that might be present in environment variables or configuration. When debugging
  with environment variables, always sanitize the output by filtering out sensitive
  keys.
repository: ghostty-org/ghostty
label: Security
language: Python
comments_count: 1
repository_stars: 32864
---

Never print or log sensitive information such as tokens, passwords, or secrets that might be present in environment variables or configuration. When debugging with environment variables, always sanitize the output by filtering out sensitive keys.

Instead of:
```python
print(*os.environ)
# or
print("token_start", repr(os.environ["GITHUB_TOKEN"][:10]))
```

Use sanitized output:
```python
print("Environment variables (sanitized):")
print({k: v for k, v in os.environ.items() if "TOKEN" not in k and "PASSWORD" not in k and "SECRET" not in k})
```

This prevents accidental exposure of credentials in logs, console output, or error reports that could lead to security breaches if captured by unauthorized parties.