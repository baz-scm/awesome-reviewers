---
title: Configure HTTP requests properly
description: When making HTTP requests, use standard library enums for status codes,
  set appropriate timeouts, and handle redirects efficiently. Avoid raw status code
  numbers in favor of HTTPStatus enums for better readability and maintainability.
  Always configure timeouts to prevent indefinite hanging, preferably making them
  configurable via environment variables with...
repository: python-poetry/poetry
label: Networking
language: Python
comments_count: 5
repository_stars: 33496
---

When making HTTP requests, use standard library enums for status codes, set appropriate timeouts, and handle redirects efficiently. Avoid raw status code numbers in favor of HTTPStatus enums for better readability and maintainability. Always configure timeouts to prevent indefinite hanging, preferably making them configurable via environment variables with sensible defaults. For upload operations, consider using HEAD requests to check for redirects before expensive POST operations to avoid retransmitting large payloads.

Example:
```python
from http import HTTPStatus
import os

# Use HTTPStatus enums instead of raw codes
if resp.status_code in (HTTPStatus.MOVED_PERMANENTLY, HTTPStatus.PERMANENT_REDIRECT):
    # handle redirect

# Configure timeouts with environment variable support
timeout = int(os.getenv('POETRY_REQUEST_TIMEOUT', 60))
response = session.get(url, timeout=timeout)

# Check for redirects before expensive operations
resp = session.head(url)
if resp.status_code == HTTPStatus.MOVED_PERMANENTLY:
    url = resp.headers['Location']
```