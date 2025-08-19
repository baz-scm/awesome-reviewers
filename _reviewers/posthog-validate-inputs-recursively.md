---
title: Validate inputs recursively
description: Always implement recursive validation and sanitization for user inputs,
  especially when dealing with encoded content or external data sources. Single-pass
  validation can be bypassed through multiple encoding layers or nested attacks.
repository: PostHog/posthog
label: Security
language: Python
comments_count: 3
repository_stars: 28460
---

Always implement recursive validation and sanitization for user inputs, especially when dealing with encoded content or external data sources. Single-pass validation can be bypassed through multiple encoding layers or nested attacks.

When validating URLs, decode recursively until no further changes occur to prevent encoding bypass attacks like `javascript%253Aalert(1)` which could decode through multiple layers to become `javascript:alert(1)`. Similarly, when integrating with external services, never trust their validation - always re-validate on your end.

Example of secure URL validation:
```python
def _is_safe_url(self, url: str) -> bool:
    """Validate URL with recursive decoding to prevent bypass attacks."""
    # Recursively decode until no changes to prevent encoding bypasses
    decoded = url
    while True:
        new_decoded = unquote(decoded)
        if new_decoded == decoded:
            break
        decoded = new_decoded
    
    # Now validate the fully decoded URL
    parsed = urlparse(decoded.lower())
    return parsed.scheme in self.ALLOWED_SCHEMES
```

This approach prevents attackers from using multiple encoding layers to bypass validation and ensures that external data sources are not blindly trusted for security-critical decisions like email verification status.