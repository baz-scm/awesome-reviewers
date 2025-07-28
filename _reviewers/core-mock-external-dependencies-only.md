---
title: Mock external dependencies only
description: When writing tests for Home Assistant integrations, mock external library
  dependencies rather than Home Assistant internals like coordinators, entities, or
  config entries. Test integration behavior through proper setup and service calls
  instead of directly manipulating internal objects.
repository: home-assistant/core
label: Testing
language: Python
comments_count: 11
repository_stars: 80450
---

When writing tests for Home Assistant integrations, mock external library dependencies rather than Home Assistant internals like coordinators, entities, or config entries. Test integration behavior through proper setup and service calls instead of directly manipulating internal objects.

**What to mock:**
- External API clients and libraries your integration depends on
- Network calls, file system operations, and other I/O
- Third-party services and hardware interfaces

**What NOT to mock:**
- Home Assistant coordinators, entities, or platforms
- Config entries, entity registry, or device registry
- Home Assistant's internal service layer

**How to test:**
- Set up the integration normally using `config_entry.add_to_hass(hass)` and `hass.config_entries.async_setup()`
- Use `hass.services.async_call()` to simulate user interactions
- Verify behavior through entity states and service call effects
- Test error conditions by making your mocked external library raise exceptions

**Example:**
```python
# ❌ Don't mock HA internals
@pytest.fixture
def mock_coordinator():
    coordinator = Mock(spec=MyDataUpdateCoordinator)
    coordinator.data = {"device_1": {"state": "on"}}
    return coordinator

# ✅ Mock external library instead
@pytest.fixture
def mock_api_client():
    with patch("my_integration.MyAPIClient") as mock:
        client = mock.return_value
        client.get_devices.return_value = [{"id": "device_1", "state": "on"}]
        client.set_device_state = AsyncMock()
        yield client

# ✅ Test through service calls
async def test_turn_on_device(hass, mock_api_client, config_entry):
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    
    await hass.services.async_call(
        "switch", "turn_on", {"entity_id": "switch.my_device"}, blocking=True
    )
    
    mock_api_client.set_device_state.assert_called_once_with("device_1", True)
```

This approach ensures tests verify actual integration behavior rather than implementation details, making them more robust and meaningful.