---
title: Prefer simpler expressions
description: "Always choose the simplest, most readable way to express your code logic.\
  \ Unnecessary complexity makes code harder to understand and maintain. \n\nWhen\
  \ writing conditionals, method calls, or data transformations, ask yourself: \"\
  Is there a clearer way to express this?\""
repository: rails/rails
label: Code Style
language: Ruby
comments_count: 6
repository_stars: 57027
---

Always choose the simplest, most readable way to express your code logic. Unnecessary complexity makes code harder to understand and maintain. 

When writing conditionals, method calls, or data transformations, ask yourself: "Is there a clearer way to express this?"

Examples of simplifying expressions:

1. Remove redundant conditionals when context makes them obvious:
```ruby
# Instead of this
if reflection.belongs_to? && model.ignored_columns.include?(reflection.foreign_key.to_s)

# Use this (when already in a belongs_to context)
if model.ignored_columns.include?(reflection.foreign_key.to_s)
```

2. Format array display consistently:
```ruby
# Instead of this verbose approach
filter_names = @filters.length == 1 ? @filters.first.inspect : "[#{@filters.map(&:inspect).join(", ")}]"

# Use the built-in inspect method
filter_names = @filters.length == 1 ? @filters.first.inspect : @filters.inspect
```

3. Use direct array methods instead of custom iterations:
```ruby
# Instead of searching with any?
unless ActiveStorage.supported_image_processing_methods.any? { |method| method_name == method }

# Use the more direct include?
unless ActiveStorage.supported_image_processing_methods.include?(method_name)
```

4. Optimize iterations when appropriate:
```ruby
# Instead of filtering then iterating
enums_to_create = columns.select { |c| c.type == :enum && c.options[:values] }
enums_to_create.each do |c|
  # process enum
end

# Check inside the loop to avoid an extra iteration
columns.each do |c|
  next unless c.type == :enum && c.options[:values]
  # process enum
end
```

5. Use modern language features when they improve readability:
```ruby
# Instead of ignoring block arguments
def add_binds(binds, proc_for_binds = nil, &_)

# Use anonymous block syntax (Ruby 2.7+)
def add_binds(binds, proc_for_binds = nil, &)
```

Remember that code is read far more often than it's written. Optimizing for readability pays dividends throughout the lifecycle of your application.
