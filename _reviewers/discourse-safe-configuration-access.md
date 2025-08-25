---
title: Safe configuration access
description: Always verify configuration properties exist before accessing them to
  prevent runtime errors. Configuration settings may not be available depending on
  installed plugins, enabled features, or user preferences.
repository: discourse/discourse
label: Configurations
language: Other
comments_count: 3
repository_stars: 44898
---

Always verify configuration properties exist before accessing them to prevent runtime errors. Configuration settings may not be available depending on installed plugins, enabled features, or user preferences.

Use appropriate safety patterns:
- For object properties: Use the `in` operator to check existence: `"saml_enabled" in this.siteSettings`
- For nested properties: Use optional chaining: `this.site.default_dark_color_scheme?.id > 0`
- For user preferences: Provide fallbacks: `this.currentUser?.user_option?.timezone || moment.tz.guess()`

This prevents crashes when accessing configuration that depends on optional plugins, feature flags, or user-specific settings that may not be present in all environments.