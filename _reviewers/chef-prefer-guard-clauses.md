---
title: Prefer guard clauses
description: Use guard clauses with early returns for null checking instead of wrapping
  code in conditional blocks. This improves readability by reducing nesting and making
  the code's "happy path" more evident.
repository: chef/chef
label: Null Handling
language: Ruby
comments_count: 5
repository_stars: 7860
---

Use guard clauses with early returns for null checking instead of wrapping code in conditional blocks. This improves readability by reducing nesting and making the code's "happy path" more evident.

```ruby
# Instead of this:
unless current_record.nil?
  current_record.status = :skipped
  current_record.conditional = conditional
end

# Do this:
return if current_record.nil?
current_record.status = :skipped
current_record.conditional = conditional
```

For method chains with potential null values, use the safe navigation operator (`&.`) instead of explicit conditional blocks:

```ruby
# Instead of:
if license_keys.nil?
  nil
else
  license_keys.empty?
end

# Do this:
license_keys&.empty?
```

When checking for truthiness, use Ruby's idiomatic style which treats only `nil` and `false` as falsey:

```ruby
# Instead of:
unless new_resource.download_url.nil?
  # code
end

# Do this:
if new_resource.download_url
  # code
end
```

Remember to use `.compact` to remove nil values from arrays when needed:

```ruby
array_with_nils.compact  # Returns a new array with all nil elements removed
```

Only use safe navigation when the object might actually be nil. Don't use it on objects that will never be nil, such as class constants:

```ruby
# Unnecessary:
::File&.dirname(path)

# Better:
::File.dirname(path)  # Since ::File will never be nil
```
