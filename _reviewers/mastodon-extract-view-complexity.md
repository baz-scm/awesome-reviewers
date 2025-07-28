---
title: Extract view complexity
description: Keep views clean and readable by extracting complex logic to appropriate
  locations. Move database queries with complex conditions to model scopes, extract
  reusable form fields to partials, and move complex conditional logic to helper methods.
repository: mastodon/mastodon
label: Code Style
language: Other
comments_count: 3
repository_stars: 48691
---

Keep views clean and readable by extracting complex logic to appropriate locations. Move database queries with complex conditions to model scopes, extract reusable form fields to partials, and move complex conditional logic to helper methods.

For database queries, use explicit ordering and create named scopes:
```ruby
# Instead of in the view:
options_from_collection_for_select(CustomEmojiCategory.order(:name).all, 'id', 'name')

# Create a model scope:
class CustomEmojiCategory
  scope :alphabetic, -> { order(name: :asc) }
end

# Then use in view:
options_from_collection_for_select(CustomEmojiCategory.alphabetic, 'id', 'name')
```

For reusable forms, extract fields to partials even for single-use forms to improve consistency and mental parsing:
```haml
# Instead of inline form fields:
= simple_form_for @generator do |form|
  .fields-group
    = form.input :field1
    = form.input :field2

# Extract to _form.html.haml:
= render 'form', generator: @generator
```

For complex conditional blocks in views, move the logic to helper methods to improve readability and testability. This separation of concerns makes views easier to scan and understand while keeping business logic properly organized.