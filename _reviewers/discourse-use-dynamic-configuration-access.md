---
title: Use dynamic configuration access
description: Always access configuration values through proper service APIs rather
  than hardcoding them or using unreliable access patterns. This ensures configuration
  remains maintainable and behaves consistently across different contexts.
repository: discourse/discourse
label: Configurations
language: JavaScript
comments_count: 4
repository_stars: 44898
---

Always access configuration values through proper service APIs rather than hardcoding them or using unreliable access patterns. This ensures configuration remains maintainable and behaves consistently across different contexts.

When accessing site settings or configuration values:
- Use established service patterns like `site` service for configuration lookup
- Avoid hardcoding configuration arrays or objects directly in code
- Prefer reliable configuration access methods over workarounds

Example of proper configuration access:
```javascript
// Instead of hardcoding:
const response = await ajax("/hashtags", {
  data: { slugs, order: ["category", "channel", "tag"] },
});

// Use service-based lookup:
const response = await ajax("/hashtags", {
  data: { slugs, order: this.site.hashtag_configurations.order },
});
```

This approach prevents issues where "the value was always false even when the site setting was true" and eliminates the need for temporary hardcoded values that developers "forgot to go back and replace."