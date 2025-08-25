---
title: API parameter clarity
description: Design API parameters with clear naming, structured formats, and intuitive
  interfaces that are easy for clients to use and maintain. Avoid complex string parsing,
  ambiguous parameter names, or structures that require clients to perform additional
  processing.
repository: discourse/discourse
label: API
language: Ruby
comments_count: 4
repository_stars: 44898
---

Design API parameters with clear naming, structured formats, and intuitive interfaces that are easy for clients to use and maintain. Avoid complex string parsing, ambiguous parameter names, or structures that require clients to perform additional processing.

Key principles:
- Use descriptive, unambiguous parameter names that clearly indicate their purpose
- Prefer structured parameter formats (hashes, objects) over string-based query languages that require regex parsing
- Design plugin APIs with clear signatures that accept the expected parameters directly
- Consider client usability when designing parameter passing (e.g., pre-filling forms with passed data)

Example of good parameter design:
```ruby
# Good: Clear parameter structure
plugin.register_modifier(:similar_topic_candidate_ids) do |existing_ids, args|
  # args contains structured data that's easy to access
  args[:candidates] # Clear what this contains
end

# Good: Structured options instead of string parsing
options_hash = {
  status: options[:status],
  category: options[:category]
}
TopicsFilter.new(scope: result, guardian: @guardian).filter(options_hash)
```

Example of problematic parameter design:
```ruby
# Problematic: Unclear parameter names and string manipulation
plugin.register_modifier(:modifier_name) do |plugin_candidate_ids, title, raw, guardian|
  # Unclear what plugin_candidate_ids contains
end

# Problematic: String parsing instead of structured data
options[:q] ||= +""
options[:q] << " status:#{status}" # Requires regex parsing later
```

This approach makes APIs more maintainable, reduces parsing complexity, and improves the developer experience for API consumers.