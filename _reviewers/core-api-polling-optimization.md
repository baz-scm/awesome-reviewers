---
title: API polling optimization
description: Optimize API polling patterns to avoid excessive calls and improve performance.
  Use appropriate update intervals based on data freshness requirements rather than
  aggressive polling schedules.
repository: home-assistant/core
label: API
language: Python
comments_count: 3
repository_stars: 80450
---

Optimize API polling patterns to avoid excessive calls and improve performance. Use appropriate update intervals based on data freshness requirements rather than aggressive polling schedules.

Key principles:
- Avoid unnecessarily frequent polling intervals (e.g., 5-second intervals for device status)
- Implement coordinators to centralize API data management and prevent overlapping calls
- Consider on-demand updates instead of scheduled polling when appropriate
- Group related API calls to minimize total requests

Example of problematic polling:
```python
super().__init__(
    hass,
    _LOGGER,
    name=DOMAIN,
    update_interval=timedelta(seconds=5),  # Too frequent!
)
```

Better approach using coordinator with reasonable intervals:
```python
class DeviceDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api: DeviceAPI):
        super().__init__(
            hass,
            _LOGGER,
            name="device_coordinator",
            update_interval=timedelta(minutes=15),  # More reasonable
        )
        self.api = api

    async def _async_update_data(self):
        # Group multiple API calls together
        return await self.api.get_all_device_data()
```

This approach reduces API rate limit issues, improves performance, and provides better user experience while future-proofing for additional platforms.