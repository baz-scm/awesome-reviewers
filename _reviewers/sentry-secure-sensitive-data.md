---
title: Secure sensitive data
description: 'Always protect sensitive data through proper encryption, secure cookies,
  and careful exception handling to prevent information leakage.


  When handling sensitive data:'
repository: getsentry/sentry
label: Security
language: Python
comments_count: 5
repository_stars: 41297
---

Always protect sensitive data through proper encryption, secure cookies, and careful exception handling to prevent information leakage.

When handling sensitive data:

1. **Use secure cookie attributes** - Always set Secure and HttpOnly flags for cookies containing sensitive information:
```python
response.set_cookie(
    settings.CSRF_COOKIE_NAME,
    request.META.get("CSRF_COOKIE"),
    secure=True,
    httponly=True,
    samesite='Lax',
    domain=settings.CSRF_COOKIE_DOMAIN,
)
```

2. **Encrypt sensitive credentials** - Use proper cryptographic methods for storing or transmitting API keys, tokens, and other secrets:
```python
# Generate cryptographically secure key
key = Fernet.generate_key()  # Returns base64 encoded key ready for use

# Use Fernet for encryption
fernet = Fernet(key)
encrypted_token = fernet.encrypt(token.encode("utf-8"))
```

3. **Prevent information leakage in exceptions** - Avoid exposing stack traces or internal details to users:
```python
# Don't do this:
raise ParseError(detail=str(e))  # May leak sensitive information

# Instead, use controlled error messages:
raise ParseError(detail="Invalid or missing date range")
```

These practices help protect your application from various security vulnerabilities including session hijacking, credential exposure, and information disclosure.