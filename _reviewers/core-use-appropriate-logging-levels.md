---
title: Use appropriate logging levels
description: 'Choose the correct logging level based on the nature and expected frequency
  of the event being logged. Follow these guidelines:


  **Use `debug` for application events:** The `info` level is reserved for system-level
  messages. Use `debug` for application-specific information like successful authentication,
  data processing steps, or operational status updates.'
repository: home-assistant/core
label: Logging
language: Python
comments_count: 6
repository_stars: 80450
---

Choose the correct logging level based on the nature and expected frequency of the event being logged. Follow these guidelines:

**Use `debug` for application events:** The `info` level is reserved for system-level messages. Use `debug` for application-specific information like successful authentication, data processing steps, or operational status updates.

**Reserve `exception` for unexpected errors:** Use `_LOGGER.exception()` only when you truly need the full stack trace to understand what went wrong - typically for unexpected errors where the system cannot continue normally. For expected errors like authentication failures or connection timeouts, use `warning` or `error` instead.

**Avoid duplicate logging:** Don't log the same event with both `exception` and `error`. Choose one based on whether you need the stack trace.

**Example of proper level usage:**
```python
try:
    client = HannaCloudClient()
    await client.authenticate(email, password, code)
    _LOGGER.debug("Authentication successful for user %s", email)
except (Timeout, RequestsConnectionError):
    _LOGGER.warning("Connection timeout during authentication")
    errors["base"] = "cannot_connect"
except AuthenticationError:
    _LOGGER.warning("Authentication failed for user %s", email)
    errors["base"] = "invalid_auth"
except Exception:
    _LOGGER.exception("Unexpected error during authentication")
    errors["base"] = "unknown"
```

This approach ensures logs are appropriately categorized, reduces noise in production logs, and provides meaningful stack traces only when needed for debugging unexpected issues.