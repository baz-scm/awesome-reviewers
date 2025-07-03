---
title: Place configurations appropriately
description: 'Choose the right location and scope for your Rails configuration options
  to improve maintainability and clarity:


  1. **Use appropriate namespaces** - For truly global configurations, place them
  on the module rather than on a specific class:'
repository: rails/rails
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 57027
---

Choose the right location and scope for your Rails configuration options to improve maintainability and clarity:

1. **Use appropriate namespaces** - For truly global configurations, place them on the module rather than on a specific class:
```ruby
# Preferred for global settings
ActiveRecord.configuration_option = value

# Avoid for global settings
ActiveRecord::Base.configuration_option = value
```

2. **Use environment-specific files** for environment-specific configurations:
```ruby
# config/environments/development.rb
config.active_record.verbose_query_logs = true
```

3. **Use load hooks** for adapter-specific configurations:
```ruby
# config/application.rb or an initializer
ActiveSupport.on_load(:active_record_postgresqladapter) do
  self.datetime_type = :timestamptz
end
```

4. **Prefer simplified syntax** when available:
```ruby
# Instead of
config.yjit = true
config.yjit_options = { stats: true }

# Prefer
config.yjit = { stats: true }
```

Using appropriate configuration placement improves organization, reduces conflicts between environments, and makes your application more maintainable.
