---
title: Write complete API examples
description: Always provide complete, context-rich code examples in API documentation.
  Examples should show the full usage context and avoid abbreviated or partial code
  snippets that may confuse developers.
repository: rails/rails
label: Documentation
language: Ruby
comments_count: 5
repository_stars: 57027
---

Always provide complete, context-rich code examples in API documentation. Examples should show the full usage context and avoid abbreviated or partial code snippets that may confuse developers.

Key guidelines:
- Show the complete context (e.g., wrapping code in create_table blocks)
- Avoid interactive prompts (like irb>)
- Use proper formatting tags for code containing spaces (<tt>)
- Include realistic variable names and values

Example:
```ruby
# ❌ Unclear context
t.bigint :account_id

# ✅ Complete context
create_table :subscriptions do |t|
  t.bigint :account_id
  t.bigint :event_ids, array: true, default: []
end
```
