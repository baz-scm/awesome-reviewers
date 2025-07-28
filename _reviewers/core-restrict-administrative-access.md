---
title: Restrict administrative access
description: Implement proper authorization controls for sensitive operations that
  can modify system configuration or create new entries. Administrative functions
  like service calls that create config entries should be restricted to admin-level
  access at minimum, or better yet, exposed as scoped integration APIs rather than
  general-purpose services. Additionally, ensure...
repository: home-assistant/core
label: Security
language: Python
comments_count: 2
repository_stars: 80450
---

Implement proper authorization controls for sensitive operations that can modify system configuration or create new entries. Administrative functions like service calls that create config entries should be restricted to admin-level access at minimum, or better yet, exposed as scoped integration APIs rather than general-purpose services. Additionally, ensure that authentication flows are thoroughly tested to verify that reauth mechanisms trigger correctly when authorization fails.

Example of problematic code:
```python
# Unrestricted service that can create config entries
hass.services.async_register(
    DOMAIN,
    "register_irk", 
    service_register_irk,
    vol.Schema({vol.Required("irk"): cv.string}),
    supports_response=SupportsResponse.NONE,
)
```

Better approach:
```python
# Restrict to admin access or expose as integration API
hass.services.async_register(
    DOMAIN,
    "register_irk",
    service_register_irk, 
    vol.Schema({vol.Required("irk"): cv.string}),
    supports_response=SupportsResponse.NONE,
    required_features=[FEATURE_ADMIN_ACCESS]  # Restrict access
)
```

Always test that reauth flows trigger properly:
```python
async def test_token_refresh_reauth():
    aioclient_mock.post(TOKEN_URL, status=HTTPStatus.UNAUTHORIZED)
    assert not await setup_integration()
    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR
    # Verify reauth flow has started
    assert len(hass.config_entries.flow.async_progress()) == 1
```