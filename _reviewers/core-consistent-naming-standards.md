---
title: Consistent naming standards
description: Ensure all user-facing strings follow Home Assistant's naming conventions
  for consistency and proper internationalization. This includes using sentence-case
  for translatable strings, proper spelling and capitalization of technical terms,
  and leveraging common string references where available.
repository: home-assistant/core
label: Naming Conventions
language: Json
comments_count: 14
repository_stars: 80450
---

Ensure all user-facing strings follow Home Assistant's naming conventions for consistency and proper internationalization. This includes using sentence-case for translatable strings, proper spelling and capitalization of technical terms, and leveraging common string references where available.

Key requirements:
- Use sentence-case for all translatable strings: "Network role" not "Network Role"
- Capitalize abbreviations consistently: "API key", "VIN", "URL", "ID"
- Use correct spelling: "IFTTT" not "IFTT", "Unsynchronized" not "Unsynchronised"
- Prefer standard terminology: "Maximum/Minimum" over "Maximal/Minimal"
- Leverage common string references: `"[%key:common::state::charging%]"` instead of custom "Charging"
- Write out unclear abbreviations: "Trip manual average speed" instead of "TM avg. speed"

Example corrections:
```json
// Before
"name": "Network Role"
"api_key": "API key"
"charging_system_charging": "Charging"

// After  
"name": "Network role"
"api_key": "[%key:common::config_flow::data::api_key%]"
"charging_system_charging": "[%key:common::state::charging%]"
```

This ensures consistent user experience across the platform and enables proper translation workflows.