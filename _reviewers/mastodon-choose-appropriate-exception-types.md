---
title: Choose appropriate exception types
description: Select exception types that match method contracts and avoid surprising
  behavior. Methods with names like `find_or_initialize_by_*` should not raise validation
  errors since the standard Rails method doesn't perform validation. Use `save` instead
  of `save!` when you want to handle validation errors gracefully rather than raising
  exceptions. Prefer standard...
repository: mastodon/mastodon
label: Error Handling
language: Ruby
comments_count: 3
repository_stars: 48691
---

Select exception types that match method contracts and avoid surprising behavior. Methods with names like `find_or_initialize_by_*` should not raise validation errors since the standard Rails method doesn't perform validation. Use `save` instead of `save!` when you want to handle validation errors gracefully rather than raising exceptions. Prefer standard exception types like `ArgumentError` for invalid parameters over custom exceptions when possible.

```ruby
# Avoid - surprising exception from find_or_initialize method
def self.find_or_initialize_by_domain(domain)
  normalized_domain = TagManager.instance.normalize_domain(domain&.strip)
  raise ActiveRecord::RecordInvalid if normalized_domain.blank?  # Surprising!
end

# Better - use appropriate exception type or remove the method
def self.find_or_initialize_by_domain(domain)
  normalized_domain = TagManager.instance.normalize_domain(domain&.strip)
  raise ArgumentError, "Invalid domain" if normalized_domain.blank?
end

# Avoid - save! raises exceptions instead of allowing error handling
tag.save!  # Causes bogus 422 responses

# Better - use save for graceful error handling
tag.save   # Allows proper error annotation on the model
```

Consider reusing existing exception classes like `Mastodon::ValidatorError` instead of creating new custom exceptions when the behavior matches existing patterns.