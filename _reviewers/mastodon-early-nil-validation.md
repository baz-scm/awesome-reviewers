---
title: early nil validation
description: Check for nil values early in methods and handle them gracefully before
  they can cause runtime errors or trigger expensive operations. This prevents NoMethodError
  exceptions and improves performance by avoiding unnecessary processing.
repository: mastodon/mastodon
label: Null Handling
language: Ruby
comments_count: 5
repository_stars: 48691
---

Check for nil values early in methods and handle them gracefully before they can cause runtime errors or trigger expensive operations. This prevents NoMethodError exceptions and improves performance by avoiding unnecessary processing.

Key patterns to implement:
- Add nil checks at the beginning of methods before calling methods on potentially nil objects
- Use early returns to exit gracefully when required values are missing
- Place nil validations before expensive operations like database queries or Redis locks
- Use conditional access patterns when objects might be nil

Example of the problem:
```ruby
def effective?
  published? && effective_date.past?  # NoMethodError if effective_date is nil
end
```

Example of the solution:
```ruby
def accept_embedded_quote_request
  quoted_status_uri = value_or_id(@object['object'])
  quoting_status_uri = value_or_id(@object['instrument'])
  approval_uri = value_or_id(first_of_value(@json['result']))
  return if quoted_status_uri.nil? || quoting_status_uri.nil? || approval_uri.nil?
  
  # Continue with expensive operations only after nil validation
  with_redis_lock("announce:#{value_or_id(@object)}") do
    # ... rest of method
  end
end
```

For conditional access to potentially nil objects:
```ruby
# Safe conditional access
cached[key] || (uncached[shortcode] if uncached)

# Safe method checking
params[scope].respond_to?(:[]) && params[scope][:password].present?
```