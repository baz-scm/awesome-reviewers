---
title: Extract duplicate code
description: When you notice repeated code patterns, logic blocks, or similar implementations
  across methods or classes, extract the common functionality into reusable methods
  or utilities. This improves maintainability, reduces bugs, and makes the codebase
  more consistent.
repository: discourse/discourse
label: Code Style
language: Ruby
comments_count: 5
repository_stars: 44898
---

When you notice repeated code patterns, logic blocks, or similar implementations across methods or classes, extract the common functionality into reusable methods or utilities. This improves maintainability, reduces bugs, and makes the codebase more consistent.

Look for these common duplication patterns:
- Similar conditional logic blocks that could be extracted into a shared method
- Repeated boilerplate code that could be centralized into a utility method  
- Multiple instances of similar object creation that could use a factory method
- Repeated test setup code that could be moved into helper methods

Example of extracting duplicate conditional logic:

```ruby
# Before: Duplicate logic in filter_users and filter_groups
def filter_users(values:)
  values.each do |value|
    if value.include?("+")
      usernames = value.split("+")
      require_all = true
      if value.include?(",")
        @scope = @scope.none
        next
      end
    else
      usernames = value.split(",")
      require_all = false
      if value.include?("+")
        @scope = @scope.none
        next
      end
    end
    # ... rest of logic
  end
end

# After: Extract common pattern
def filter_users(values:)
  values.each do |value|
    usernames, require_all = parse_filter_value(value)
    next if usernames.nil?
    # ... rest of user-specific logic
  end
end

private

def parse_filter_value(value)
  if value.include?("+") && value.include?(",")
    @scope = @scope.none
    return [nil, nil]
  end
  
  if value.include?("+")
    [value.split("+"), true]
  else
    [value.split(","), false]
  end
end
```

Before implementing new functionality, check if similar logic already exists that could be reused or if the new code could be designed to share common patterns with existing implementations.