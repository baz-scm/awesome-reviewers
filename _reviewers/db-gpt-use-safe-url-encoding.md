---
title: Use safe URL encoding
description: When constructing connection strings/URIs that embed user credentials,
  always URL-encode username/password (and other URI components as needed) using an
  encoder that safely handles reserved characters. Avoid `urllib.parse.quote` for
  credentials where characters like `@` and `#` may appear; prefer `quote_plus`.
repository: eosphoros-ai/DB-GPT
label: Security
language: Python
comments_count: 1
repository_stars: 18703
---

When constructing connection strings/URIs that embed user credentials, always URL-encode username/password (and other URI components as needed) using an encoder that safely handles reserved characters. Avoid `urllib.parse.quote` for credentials where characters like `@` and `#` may appear; prefer `quote_plus`.

Example:
```python
from urllib.parse import quote_plus

db_url = (
    f"doris://{quote_plus(user)}:{quote_plus(pwd)}@{host}:{port}/{db_name}"
)
```

This prevents malformed URIs and ensures credentials are interpreted correctly and securely by the client/driver.