---
title: Avoid Logging Sensitive Data
description: Do not log raw function parameters (e.g., `kwargs`, request bodies, headers,
  tokens, credentials, or any data that could include PII). Logging can expose sensitive
  information via application logs, monitoring systems, or log sharing.
repository: Azure/Azure-Sentinel
label: Security
language: Python
comments_count: 1
repository_stars: 6042
---

Do not log raw function parameters (e.g., `kwargs`, request bodies, headers, tokens, credentials, or any data that could include PII). Logging can expose sensitive information via application logs, monitoring systems, or log sharing.

Apply this rule:
- Prefer logging only safe, non-sensitive metadata (e.g., request ID, operation name, status codes).
- If you must log values for debugging, redact or whitelist fields before logging.

Example (safe pattern):
```python
# BAD: may contain secrets/PII
# logging.info(f"Parameters: {kwargs}")

# GOOD: log only non-sensitive metadata
logging.info("Calling function to get AWS SSM Inventory")

# If needed, log a sanitized subset
safe = {k: v for k, v in kwargs.items() if k in {"region", "page"} }
logging.info(f"Request metadata: {safe}")
```

Enforce this especially in security-sensitive code paths (auth flows, AWS connectors, inventory/config fetchers, and anything handling user input).