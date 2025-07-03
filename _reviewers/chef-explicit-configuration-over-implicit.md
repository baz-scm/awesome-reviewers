---
title: Explicit configuration over implicit
description: 'Always define explicit configuration defaults rather than relying on
  implicit behavior or autovivification. Configuration values should:


  1. Use explicit nil defaults instead of undefined values'
repository: chef/chef
label: Configurations
language: Ruby
comments_count: 5
repository_stars: 7860
---

Always define explicit configuration defaults rather than relying on implicit behavior or autovivification. Configuration values should:

1. Use explicit nil defaults instead of undefined values
2. Document default values clearly in property descriptions
3. Use Chef::Config for global settings rather than environment variables
4. Consider platform-specific variations when defining defaults

Example:
```ruby
# Bad - Implicit default
property :store_location, String

# Good - Explicit default with clear documentation
property :store_location, String,
  default: nil,
  description: "Use the `CurrentUser` store instead of the default `LocalMachine` store."

# Bad - Environment variable configuration
default :use_s3_cache, ENV['USE_S3_CACHE'] == 'true'

# Good - Chef::Config configuration
config_context :caching do
  default :use_s3, false
end
```

This approach improves code clarity, makes behavior more predictable, and ensures proper documentation of configuration options. It also facilitates better testing and maintenance by making all possible states explicit.
