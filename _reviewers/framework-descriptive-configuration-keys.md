---
title: Descriptive configuration keys
description: Configuration keys should clearly indicate their value type, units, or
  expected format to prevent misunderstandings and errors. Include unit information
  directly in key names when appropriate and ensure documentation accurately reflects
  the default values and behavior.
repository: laravel/framework
label: Configurations
language: PHP
comments_count: 4
repository_stars: 33763
---

Configuration keys should clearly indicate their value type, units, or expected format to prevent misunderstandings and errors. Include unit information directly in key names when appropriate and ensure documentation accurately reflects the default values and behavior.

For example, instead of using a generic key with ambiguous units:

```php
// Unclear - are these hours or minutes?
'maintenance_bypass_cookie_lifetime' => (int) env('SESSION_MAINTENANCE_BYPASS_COOKIE_LIFETIME', 720),
```

Use a more descriptive key that includes the unit:

```php
'maintenance_bypass_cookie_lifetime_minutes' => (int) env('SESSION_MAINTENANCE_BYPASS_COOKIE_LIFETIME_MINUTES', 720),
```

This approach makes configuration self-documenting, reduces the need to consult documentation, and prevents errors from unit mismatches or incorrect assumptions about value types. When environment variables serve as configuration sources, maintain this same naming convention to ensure consistency across your application's configuration system.
