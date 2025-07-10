---
title: Optimize collection operations
description: Use Ruby's built-in collection methods to write more efficient and readable
  code. This reduces algorithmic complexity and improves performance by leveraging
  optimized implementations instead of writing manual iterations or chaining multiple
  operations.
repository: Homebrew/brew
label: Algorithms
language: Ruby
comments_count: 7
repository_stars: 44168
---

Use Ruby's built-in collection methods to write more efficient and readable code. This reduces algorithmic complexity and improves performance by leveraging optimized implementations instead of writing manual iterations or chaining multiple operations.

Specifically:

1. Use destructive methods with exclamation points when modifying collections in-place:
```ruby
# Instead of:
upgradeable = upgradeable.reject { |f| FormulaInstaller.installed.to_a.include?(f) }

# Prefer:
upgradeable.reject! { |f| FormulaInstaller.installed.include?(f) }
```

2. Use array operations and splats for manipulation instead of multiple method calls:
```ruby
# Instead of:
json["old_tokens"] = (json["old_tokens"] << old_token).uniq

# Prefer:
json["old_tokens"] = [old_token, *json["old_tokens"]].compact.uniq
```

3. Use Symbol#to_proc syntax with methods like `map` and `filter_map` to create more concise code:
```ruby
# Instead of:
installed_formula_tap_names = Formula.installed.map { |f| f.tap.name }
                                    .reject { |name| name == "homebrew/core" }.uniq

# Prefer:
installed_formula_tap_names = Formula.installed.filter_map(&:tap).uniq.reject(&:official?)
```

4. Consider memoization for expensive operations that may be called repeatedly:
```ruby
# Instead of:
def non_core_taps
  Tap.installed.reject(&:core_tap?).reject(&:core_cask_tap?)
end

# Prefer:
def non_core_taps
  @non_core_taps ||= Tap.installed.reject(&:core_tap?).reject(&:core_cask_tap?)
end
```

These approaches lead to faster algorithms, reduced memory usage, and more maintainable code.