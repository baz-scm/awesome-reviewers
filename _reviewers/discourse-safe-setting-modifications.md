---
title: Safe setting modifications
description: When modifying site settings during operations like imports, jobs, or
  plugin initialization, implement proper safeguards to prevent unintended permanent
  changes. Consider the impact on existing sites and provide mechanisms for restoration
  or warnings.
repository: discourse/discourse
label: Configurations
language: Ruby
comments_count: 4
repository_stars: 44898
---

When modifying site settings during operations like imports, jobs, or plugin initialization, implement proper safeguards to prevent unintended permanent changes. Consider the impact on existing sites and provide mechanisms for restoration or warnings.

Key practices:
- Wrap temporary setting changes in restore logic or dedicated configuration steps
- Query actual data requirements before adjusting settings (e.g., check maximum tag length before setting `max_tag_length`)
- Set conditional defaults based on plugin availability rather than hardcoded values
- Use centralized default configuration patterns like `USER_OPTION_DEFAULTS` instead of inline hardcoded values
- Provide warnings when settings will be modified, especially during imports to existing sites

Example from tag import:
```ruby
# Instead of hardcoding:
SiteSetting.max_tag_length = 100 if SiteSetting.max_tag_length < 100

# Query actual requirements:
max_tag_length_needed = source_db.query("SELECT MAX(LENGTH(name)) FROM tags").first
SiteSetting.max_tag_length = max_tag_length_needed if SiteSetting.max_tag_length < max_tag_length_needed
```

Example for conditional defaults:
```ruby
# In base configuration:
USER_OPTION_DEFAULTS = {
  hide_profile: SiteSetting.default_hide_profile,
  assignable_level: Group::ALIAS_LEVELS[:nobody] # Set unconditionally with comment explaining why
}
```

This approach prevents configuration drift, reduces surprises for site administrators, and makes operations more predictable across different environments.