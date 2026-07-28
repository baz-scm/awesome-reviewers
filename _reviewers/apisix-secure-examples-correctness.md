---
title: Secure examples correctness
description: 'When implementing or documenting security-related plugins/features,
  ensure examples are both *secure* and *operationally correct*: avoid leaking sensitive
  data, match cookie/transport settings, use the correct authentication header formats,
  and ensure authentication happens before authorization/restriction.'
repository: apache/apisix
label: Security
language: Markdown
comments_count: 5
repository_stars: 16922
---

When implementing or documenting security-related plugins/features, ensure examples are both *secure* and *operationally correct*: avoid leaking sensitive data, match cookie/transport settings, use the correct authentication header formats, and ensure authentication happens before authorization/restriction.

Apply these rules:
- **Redact/flag sensitive inputs**: If a feature can forward request bodies or headers (e.g., `with_body`), explicitly warn that it may contain secrets (passwords/API keys) and ensure the option is used only when safe.
- **Match Secure transport semantics**: If cookies/sessions are configured with `secure=true`, examples must use **HTTPS** or explicitly set `secure=false` for local HTTP testing.
- **Use correct auth header scheme**: For bearer tokens, always set `Authorization: Bearer <token>` (not just the raw token).
- **Auth before authz**: Authorization/restriction logic must run only after the identity is resolved by an authentication plugin; examples should configure auth (e.g., `key-auth`) so the Consumer is determined before applying restriction rules.

Example (Bearer token correctness):
```sh
curl -i "http://127.0.0.1:9080/get" \
  -H "Authorization: Bearer ${john_jwt_token}"
```

Example (Secure cookie guidance):
- For **HTTPS** examples: keep `cookie.secure=true`.
- For **HTTP** local testing: set `cookie.secure=false` or switch the example to HTTPS.

Example (auth-before-restriction):
- Configure an authentication plugin (e.g., `key-auth`) so the gateway can resolve the Consumer, then apply `consumer-restriction` based on that resolved identity.