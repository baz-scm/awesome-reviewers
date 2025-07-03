---
title: Choose semantic algorithms
description: Select algorithms and data operations that match the semantic intent
  of your code rather than using convenient but potentially problematic approaches.
  For operations like version comparisons, string parsing, and collection filtering,
  choose specialized methods over generic ones.
repository: chef/chef
label: Algorithms
language: Ruby
comments_count: 6
repository_stars: 7860
---

Select algorithms and data operations that match the semantic intent of your code rather than using convenient but potentially problematic approaches. For operations like version comparisons, string parsing, and collection filtering, choose specialized methods over generic ones.

For version comparisons:
```ruby
# Avoid unreliable approaches like timestamp comparison
# BAD
latest_version_dir = versions.max_by { |v| File.mtime(v) } 

# GOOD - Use semantic version comparison
latest_version_dir = versions.max_by { |v| Gem::Version.new(File.basename(v)) }
```

For string parsing, prefer structured operations over complex regex when appropriate:
```ruby
# Overly complex regex
z = t.match(/(^pub:.?:\d*:\d*:\w*:[\d-]*):/)

# More maintainable approach
fields = t.split(':')
z = fields[0..4].join(':') if fields.size >= 5
```

For collection operations, choose methods that properly handle the data structure:
```ruby
# Limited to checking a single action
options[:required].include?(action)

# Properly handles multiple actions
(options[:required] & Array(action)).any?
```

Remember that algorithm selection significantly impacts code reliability, maintainability, and performance. Choose algorithms that reflect the true intent of the operation rather than just what seems convenient.
