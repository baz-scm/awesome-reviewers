---
title: Use configuration constants
description: Always use predefined constants from `homeassistant.const` instead of
  string literals when accessing configuration data. For required configuration keys
  that must be present, use direct dictionary access (`entry.data[CONF_KEY]`) rather
  than `.get()` with defaults, as this provides better error handling and makes the
  required nature of the configuration...
repository: home-assistant/core
label: Configurations
language: Python
comments_count: 3
repository_stars: 80450
---

Always use predefined constants from `homeassistant.const` instead of string literals when accessing configuration data. For required configuration keys that must be present, use direct dictionary access (`entry.data[CONF_KEY]`) rather than `.get()` with defaults, as this provides better error handling and makes the required nature of the configuration explicit.

```python
# Bad - using string literals and .get() for required keys
email = user_input.get("email")
password = user_input.get("password") 
api_key = entry.data.get("api_key", "")

# Good - using constants and direct access for required keys
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_API_KEY

email = user_input.get(CONF_EMAIL)
password = user_input.get(CONF_PASSWORD)
api_key = entry.data[CONF_API_KEY]  # Will raise KeyError if missing, which is appropriate
```

This approach improves code maintainability, prevents typos in configuration key names, and makes the required vs optional nature of configuration values clear through the access pattern used.