---
title: Human-readable configuration values
description: When writing configuration files, prioritize human readability and maintainability
  by using descriptive expressions instead of magic numbers or cryptic values. This
  makes code more understandable and easier to maintain.
repository: rails/rails
label: Configurations
language: Other
comments_count: 4
repository_stars: 57027
---

When writing configuration files, prioritize human readability and maintainability by using descriptive expressions instead of magic numbers or cryptic values. This makes code more understandable and easier to maintain.

For time-based configurations, prefer using expressions like `1.year.to_i` or `1.hour.to_i` instead of hard-coded seconds:

```ruby
# Avoid this
config.public_file_server.headers = { "cache-control" => "public, max-age=31556952" }

# Prefer this
config.public_file_server.headers = { "cache-control" => "public, max-age=#{1.year.to_i}" }
```

Keep configuration formatting consistent and pay attention to spacing, especially around conditional statements:

```ruby
# Incorrect
t.options = "--profile"if ENV["CI"]

# Correct
t.options = "--profile" if ENV["CI"]
```

Document configuration options clearly, especially when they relate to environment variables or external settings. Use precise language that accurately describes the expected value format:

```ruby
# Vague
# similar environment variable prefixed with the configuration key in uppercase.

# Clear and precise
# similar environment variable prefixed with the connection name appended to `DATABASE_URL`.
```

Maintaining consistent, readable configuration across all environments helps prevent unexpected behavior and makes your application easier to debug and maintain.
