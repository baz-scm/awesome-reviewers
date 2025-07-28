---
title: Use shared string keys
description: Replace hardcoded strings in configuration files with shared string key
  references to maintain consistency and enable centralized management. This practice
  reduces duplication, ensures uniform messaging across components, and makes updates
  easier to maintain.
repository: home-assistant/core
label: Configurations
language: Json
comments_count: 6
repository_stars: 80450
---

Replace hardcoded strings in configuration files with shared string key references to maintain consistency and enable centralized management. This practice reduces duplication, ensures uniform messaging across components, and makes updates easier to maintain.

Instead of using hardcoded strings:
```json
{
  "config": {
    "step": {
      "user": {
        "data": {
          "email": "Email",
          "password": "Password"
        }
      }
    },
    "abort": {
      "already_configured": "Device is already configured"
    }
  }
}
```

Use shared string key references:
```json
{
  "config": {
    "step": {
      "user": {
        "data": {
          "email": "[%key:common::config_flow::data::email%]",
          "password": "[%key:common::config_flow::data::password%]"
        }
      }
    },
    "abort": {
      "already_configured": "[%key:common::config_flow::abort::already_configured_device%]"
    }
  }
}
```

This approach allows for centralized string management, consistent terminology across the application, and easier localization. Look for existing common keys before creating new hardcoded strings, and reuse error messages and standard configuration labels wherever possible.