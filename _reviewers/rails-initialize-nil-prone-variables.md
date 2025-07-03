---
title: Initialize nil-prone variables
description: 'Always initialize variables that might be nil to appropriate default
  values to prevent unexpected behavior. For boolean flags, explicitly initialize
  to false in constructors or initialization methods:'
repository: rails/rails
label: Null Handling
language: Ruby
comments_count: 5
repository_stars: 57027
---

Always initialize variables that might be nil to appropriate default values to prevent unexpected behavior. For boolean flags, explicitly initialize to false in constructors or initialization methods:

```ruby
def initialize
  @unsubscribed = false  # Clear and explicit boolean state
end
```

For collections, initialize to empty arrays or hashes rather than nil. When setting defaults, use `||=` or `Hash#reverse_merge!` to assign values only when current value is nil:

```ruby
@options[:autocomplete] ||= "off"  # Only assigns if nil
# or
@options.reverse_merge!(autocomplete: "off")
```

When implementing predicate methods, use explicit `== true` comparison to ensure they return true or false, never nil:

```ruby
def define_predicate_method(name)
  define_method("#{name}?") { public_send(name) == true }
end
```

For complex types like JSON, provide sensible defaults:

```ruby
# When handling JSON type
when :json then {}  # Or use a more descriptive example structure
```

This proactive approach prevents nil-related errors and ensures consistent behavior throughout your application lifecycle.
