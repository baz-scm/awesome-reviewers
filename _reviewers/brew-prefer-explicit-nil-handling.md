---
title: Prefer explicit nil handling
description: 'Handle nil values explicitly and consistently to improve code clarity
  and type safety. Follow these guidelines:


  1. Use early returns for nil validation:'
repository: Homebrew/brew
label: Null Handling
language: Ruby
comments_count: 10
repository_stars: 44168
---

Handle nil values explicitly and consistently to improve code clarity and type safety. Follow these guidelines:

1. Use early returns for nil validation:
```ruby
# Bad
def process_data
  if data.present?
    # process data
  end
end

# Good
def process_data
  return if data.blank?
  # process data
end
```

2. Use .presence for nil/empty string handling:
```ruby
# Bad
name = input.empty? ? nil : input

# Good
name = input.presence
```

3. Prefer raising errors over returning nil when appropriate:
```ruby
# Bad
def fetch_config
  config = load_config
  config if config.valid?
end

# Good
def fetch_config
  config = load_config
  raise Error, "Invalid config" unless config.valid?
  config
end
```

4. Use proper type signatures for nullable values:
```ruby
# Bad
sig { returns(String) }
def optional_value
  @value # might be nil!
end

# Good
sig { returns(T.nilable(String)) }
def optional_value
  @value
end
```

This approach improves code readability, makes nil-handling intentions clear, and helps catch potential nil-related issues early through static analysis.