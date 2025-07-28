---
title: Use descriptive specific names
description: Choose descriptive, specific names that clearly communicate intent and
  behavior rather than generic or ambiguous alternatives. Names should be self-documenting
  and reduce the need for additional context or comments.
repository: mastodon/mastodon
label: Naming Conventions
language: Ruby
comments_count: 9
repository_stars: 48691
---

Choose descriptive, specific names that clearly communicate intent and behavior rather than generic or ambiguous alternatives. Names should be self-documenting and reduce the need for additional context or comments.

**Key principles:**
- **Be specific over generic**: Use `start_with?('_misskey')` instead of broad `start_with?('_')` when the intent is specific to Misskey properties
- **Clarify behavior in method names**: Use `by_language_length` instead of `by_language` when sorting by length, or `forwardable?` instead of `can_forward?` to follow Ruby predicate conventions
- **Make scope names unambiguous**: Use `category_account` instead of `account` for scopes to avoid confusion with model attributes
- **Use descriptive parameter names**: Replace generic `options = {}` with explicit `forward_to_domains = []` to clarify expected usage
- **Extract complex logic with descriptive names**: Instead of inline complex conditions, use helper methods like `last_page?` and `paginating_down?`

**Example:**
```ruby
# Avoid generic/ambiguous names
scope :account, -> { where(category: 'account') }
def can_forward?

# Use descriptive, specific names  
scope :category_account, -> { where(category: 'account') }
def forwardable?
```

This approach improves code readability, reduces cognitive load, and makes the codebase more maintainable by ensuring names accurately reflect their purpose and behavior.