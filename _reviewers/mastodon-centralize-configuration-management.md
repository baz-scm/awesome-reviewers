---
title: centralize configuration management
description: Migrate configuration from direct environment variable access to Rails'
  config_for mechanism for better organization, testability, and maintainability.
  Instead of accessing ENV variables directly throughout the codebase, consolidate
  them into YAML configuration files loaded at application startup.
repository: mastodon/mastodon
label: Configurations
language: Ruby
comments_count: 7
repository_stars: 48691
---

Migrate configuration from direct environment variable access to Rails' config_for mechanism for better organization, testability, and maintainability. Instead of accessing ENV variables directly throughout the codebase, consolidate them into YAML configuration files loaded at application startup.

**Why this matters:**
- Enables the Rails/EnvironmentVariableAccess cop to enforce "configure at load time" practices
- Centralizes configuration in one place for easier management
- Improves testability by allowing config reloading in specs
- Prevents load order issues with configuration dependencies
- Reduces duplication of configuration logic across controllers and models

**How to apply:**
1. Move ENV variable access from code to config/mastodon.yml or similar config_for files
2. Access configuration via Rails.configuration.x.namespace instead of ENV directly
3. Keep any string parsing/processing logic in the consuming classes, only move the raw ENV.fetch calls to config files
4. Maintain test coverage for environment variable effects using config reloading in specs

**Example:**
```ruby
# Before - scattered ENV access
def mfa_force_enabled?
  ENV['MFA_FORCE'] == 'true'
end

def authorized_fetch_mode?
  %w(true all).include?(ENV.fetch('AUTHORIZED_FETCH', 'false'))
end

# After - centralized in config/mastodon.yml
# mfa_force: <%= ENV.fetch('MFA_FORCE', 'false') %>
# authorized_fetch: <%= ENV.fetch('AUTHORIZED_FETCH', 'false') %>

# Then access via:
def mfa_force_enabled?
  Rails.configuration.x.mastodon.mfa_force == 'true'
end

def authorized_fetch_mode?
  %w(true all).include?(Rails.configuration.x.mastodon.authorized_fetch)
end
```

This approach consolidates configuration management while preserving the ability to test environment variable behavior and avoiding configuration logic duplication across the application.