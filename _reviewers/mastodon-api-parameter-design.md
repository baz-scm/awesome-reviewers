---
title: API parameter design
description: Design API parameters with clear intent, proper validation, and thoughtful
  default behaviors. Parameter names should reflect their purpose rather than their
  source (e.g., `include_original` instead of `client_type == 'editor'`). Always validate
  parameters through StrongParameters to prevent security issues, and carefully consider
  the implications of default...
repository: mastodon/mastodon
label: API
language: Ruby
comments_count: 5
repository_stars: 48691
---

Design API parameters with clear intent, proper validation, and thoughtful default behaviors. Parameter names should reflect their purpose rather than their source (e.g., `include_original` instead of `client_type == 'editor'`). Always validate parameters through StrongParameters to prevent security issues, and carefully consider the implications of default values - missing parameters should not trigger potentially harmful actions like forwarding to remote instances.

When evolving APIs, prefer explicit parameter migration over breaking changes. For example, redirect old parameter names to new ones while preserving all existing filters:

```ruby
# Migrate old parameter names while preserving other filters
if params.include? :by_target_domain
  redirect_to admin_reports_path({
    search_type: 'target',
    search_term: params[:by_target_domain],
    # Preserve existing status filter
    status: params[:status]
  }.compact)
end
```

Avoid implicit behaviors based on missing parameters. Instead of defaulting to potentially destructive actions, require explicit opt-in through clear parameter names that communicate intent.