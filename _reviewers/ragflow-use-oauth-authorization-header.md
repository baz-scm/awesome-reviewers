---
title: Use OAuth Authorization Header
description: When authenticating requests with bearer tokens or OAuth-derived credentials,
  transmit them using the standards-based `Authorization` request header as required
  by the relevant OAuth specification. Avoid sending secrets via custom headers like
  `api_key`, and ensure documentation/examples match the OAuth flow requirements.
repository: infiniflow/ragflow
label: Security
language: Markdown
comments_count: 1
repository_stars: 80174
---

When authenticating requests with bearer tokens or OAuth-derived credentials, transmit them using the standards-based `Authorization` request header as required by the relevant OAuth specification. Avoid sending secrets via custom headers like `api_key`, and ensure documentation/examples match the OAuth flow requirements.

Example (adapted to a typical async client):
```python
# Preferred: OAuth-compliant Authorization header
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # or the OAuth-defined scheme/value
}

async with sse_client(
    "http://localhost:9382/sse",
    headers=headers,
) as streams:
    # Rest of your code...
```

Apply this to code, SDK wrappers, and docs: if the auth method is OAuth 2.1 (or similar), use `Authorization` and the required formatting/scheme, rather than custom credential headers.