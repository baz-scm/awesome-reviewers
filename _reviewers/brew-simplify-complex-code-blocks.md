---
title: Simplify complex code blocks
description: Break down complex code blocks and expressions into simpler, more readable
  components. Complex boolean logic, nested conditions, and multi-operation lines
  should be refactored for clarity.
repository: Homebrew/brew
label: Code Style
language: Ruby
comments_count: 5
repository_stars: 44168
---

Break down complex code blocks and expressions into simpler, more readable components. Complex boolean logic, nested conditions, and multi-operation lines should be refactored for clarity.

Key practices:
1. Split complex boolean expressions into named variables or helper methods
2. Break long one-liners into multiple lines
3. Prefer positive conditions over negative ones
4. Use early returns to reduce nesting

Example - Before:
```ruby
return unless artifacts.reject do |k|
  k.is_a?(::Cask::Artifact::Font)
end.empty?
```

After:
```ruby
return if artifacts.all?(::Cask::Artifact::Font)
```

Or when dealing with complex conditions:

Before:
```ruby
print_stderr = !(verbose && show_info).nil?
```

After:
```ruby
print_stderr = if verbose && show_info
  true
else
  false
end
```

This approach makes code easier to read, understand, and maintain while reducing the cognitive load on reviewers and future maintainers.