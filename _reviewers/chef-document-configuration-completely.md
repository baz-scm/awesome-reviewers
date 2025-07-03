---
title: Document configuration completely
description: 'Always provide complete documentation for configuration options, including
  defaults, override methods, and security implications. When documenting configuration:'
repository: chef/chef
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 7860
---

Always provide complete documentation for configuration options, including defaults, override methods, and security implications. When documenting configuration:

1. Be explicit about default values and their rationale
2. Provide clear examples showing the correct syntax
3. Specify whether configurations apply locally or globally
4. Document any security considerations

For dependency-related configurations, include the exact commands and their outputs in PR descriptions:

```ruby
# Example for gem installations
gem install [gem_name] --conservative

# Example for configuration attributes
node['audit']['reporter'] = %w{json-file cli}

# Example for local-scoped bundle configurations
bundle config set --local without development
```

When configuration defaults change, especially those with security implications, provide clear migration paths for users who need previous functionality.
