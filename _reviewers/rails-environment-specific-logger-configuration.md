---
title: Environment-specific logger configuration
description: Configure loggers in environment-specific files rather than in application.rb
  or initializers. Different environments (development, test, production) typically
  require different logging levels and configurations, and Rails is designed to support
  this pattern.
repository: rails/rails
label: Logging
language: Markdown
comments_count: 3
repository_stars: 57027
---

Configure loggers in environment-specific files rather than in application.rb or initializers. Different environments (development, test, production) typically require different logging levels and configurations, and Rails is designed to support this pattern.

When setting up loggers or modifying logging levels, place the configuration in the appropriate environment file:

```ruby
# AVOID
# config/application.rb
config.logger = Logger.new(STDOUT)
config.log_level = :warn

# PREFER
# config/environments/production.rb
config.logger = Logger.new(STDOUT)
config.log_level = :warn
```

This approach ensures that each environment can have tailored logging settings appropriate for its context (e.g., verbose in development, minimal in production). It also follows Rails conventions, making your codebase more maintainable and aligned with standard practices.
