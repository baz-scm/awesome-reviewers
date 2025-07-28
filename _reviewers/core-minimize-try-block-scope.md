---
title: Minimize try block scope
description: Only include code that can actually raise exceptions within try blocks.
  Move variable assignments, logging statements, and other operations that cannot
  fail outside of the try block to avoid accidentally catching unintended exceptions
  and to improve code clarity.
repository: home-assistant/core
label: Error Handling
language: Python
comments_count: 5
repository_stars: 80450
---

Only include code that can actually raise exceptions within try blocks. Move variable assignments, logging statements, and other operations that cannot fail outside of the try block to avoid accidentally catching unintended exceptions and to improve code clarity.

This practice ensures that exception handling is precise and that you only catch the specific errors you intend to handle, rather than masking unexpected failures in seemingly safe operations.

Example of what to avoid:
```python
try:
    session = async_get_clientsession(hass)
    api = RedgtechAPI()
    access_token = await api.login(email, password)
    if access_token:
        _LOGGER.debug("Login successful, token received.")
        # ... more processing
except Exception as e:
    _LOGGER.error("Login failed: %s", e)
```

Better approach:
```python
session = async_get_clientsession(hass)
api = RedgtechAPI()
try:
    access_token = await api.login(email, password)
except Exception as e:
    _LOGGER.error("Login failed: %s", e)
    return

if access_token:
    _LOGGER.debug("Login successful, token received.")
    # ... more processing
```

By limiting the try block to only the `await api.login()` call, you ensure that any exceptions from session creation or API instantiation are not accidentally caught and mishandled as login failures.