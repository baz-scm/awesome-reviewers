---
title: Centralize shared configurations
description: Avoid duplicating configuration values across multiple files. Instead,
  define shared configurations in centralized locations and import them where needed.
  This prevents inconsistencies and makes configuration management more maintainable.
repository: juspay/hyperswitch
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 34028
---

Avoid duplicating configuration values across multiple files. Instead, define shared configurations in centralized locations and import them where needed. This prevents inconsistencies and makes configuration management more maintainable.

When the same configuration values are needed in multiple files, create a single source of truth rather than hardcoding values in each location. For example, instead of defining connector lists directly in test files:

```javascript
// Avoid: Hardcoded in test file
const UCS_SUPPORTED_CONNECTORS = ["authorizedotnet"];
```

Use centralized configuration:

```javascript
// Preferred: Import from centralized config
import { UCS_SUPPORTED_CONNECTORS } from "../../configs/Payment/Utils.js";
```

Similarly, for timeout values and other environment-specific settings, maintain consistency by using the same configuration source across related files. This approach reduces the risk of configuration drift and makes updates easier to manage.