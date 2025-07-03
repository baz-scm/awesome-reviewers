---
title: Document performance implications
description: Clearly document the performance implications of features and configurations
  to help users make informed decisions. Avoid overstating or understating performance
  impacts. Instead, provide specific context about when certain features might impact
  performance and in what environments they are appropriate.
repository: rails/rails
label: Performance Optimization
language: Markdown
comments_count: 3
repository_stars: 57027
---

Clearly document the performance implications of features and configurations to help users make informed decisions. Avoid overstating or understating performance impacts. Instead, provide specific context about when certain features might impact performance and in what environments they are appropriate.

For example, when adding a feature with potential performance impact:

```ruby
# GOOD
# In documentation:
# The :source_location option can slow down query execution, so consider its impact
# if using in production environments where query volume is high.

# BAD
# WARNING: Never use :source_location in production! It will destroy performance!

# BETTER
# When implementing configurable features:
config.feature.enabled = true # in development.rb
config.feature.enabled = false # in production.rb (default)
```

Consider providing environment-specific defaults for performance-impacting features, making them opt-in for production rather than requiring users to opt-out. When performance tradeoffs exist (like between different checksum algorithms or between observability and optimization), document these tradeoffs to help users select the most appropriate option for their specific use case.
