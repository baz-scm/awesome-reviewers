---
title: Use safe navigation operator
description: Prefer Ruby's safe navigation operator (`&.`) over explicit nil checks
  when calling methods on potentially nil objects. This approach makes code more readable,
  reduces boilerplate, and prevents NoMethodError exceptions in a clean, idiomatic
  way.
repository: discourse/discourse
label: Null Handling
language: Ruby
comments_count: 2
repository_stars: 44898
---

Prefer Ruby's safe navigation operator (`&.`) over explicit nil checks when calling methods on potentially nil objects. This approach makes code more readable, reduces boilerplate, and prevents NoMethodError exceptions in a clean, idiomatic way.

The safe navigation operator only calls the method if the object is not nil, returning nil otherwise. This eliminates the need for verbose conditional checks while maintaining null safety.

**Example:**
```ruby
# Instead of explicit nil checking:
if row[:description]
  row[:description] = sanitize_field(row[:description])[0...MAX_DESCRIPTION_LENGTH]
end

# Use safe navigation:
row[:description] = sanitize_field(row[:description])&.slice(0, MAX_DESCRIPTION_LENGTH)

# Instead of:
if @options[:used_flag_ids]
  @options[:used_flag_ids].include?(object.id)
end

# Use:
@options[:used_flag_ids]&.include?(object.id)
```

This pattern is particularly valuable in serializers, service objects, and anywhere you're working with optional parameters or potentially nil objects. It reduces cognitive load and makes the happy path more prominent in your code.