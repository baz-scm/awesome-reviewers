---
title: Document APIs clearly
description: When designing and documenting APIs, prioritize clarity and completeness
  through concrete examples and accurate parameter descriptions. Your documentation
  should help developers understand both the basic usage and edge cases of your API.
repository: rails/rails
label: API
language: Markdown
comments_count: 6
repository_stars: 57027
---

When designing and documenting APIs, prioritize clarity and completeness through concrete examples and accurate parameter descriptions. Your documentation should help developers understand both the basic usage and edge cases of your API.

For parameter documentation:
- Explain what each parameter does and its default value
- Clearly indicate parameter limitations (like when they apply)
- Use proper formatting for parameter names (e.g., `api_timestamp_field:`)

Always include practical examples:
```ruby
# Good - shows parameter usage with examples
# acts_as_api_resource api_timestamp_field: :last_api_access
#
# Example:
class Product < ApplicationRecord
  acts_as_api_resource api_timestamp_field: :last_accessed_at
end
```

When designing callback-style APIs, follow Rails conventions where possible:
```ruby
# Option 1: Named options with method references or lambdas
has_one_attached :image, after_attached: :process_image

# Option 2: Configuration within blocks
has_one_attached :image do |attachable|
  attachable.after_attached do |blob|
    process_image(blob)
  end
end
```

Keep documentation consistent across all locations (guides and API reference), with simpler cases in guides and more complex edge cases in API reference documentation. This approach ensures developers can find the right information at the right time as they progress from basic to advanced usage.
