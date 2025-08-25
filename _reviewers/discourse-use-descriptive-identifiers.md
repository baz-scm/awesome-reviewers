---
title: Use descriptive identifiers
description: Choose names that clearly communicate purpose and reduce cognitive load
  for future readers. Avoid generic, abbreviated, or ambiguous identifiers in favor
  of self-documenting ones.
repository: discourse/discourse
label: Naming Conventions
language: Ruby
comments_count: 12
repository_stars: 44898
---

Choose names that clearly communicate purpose and reduce cognitive load for future readers. Avoid generic, abbreviated, or ambiguous identifiers in favor of self-documenting ones.

**Key principles:**
- **Variables**: Use descriptive names that indicate content and purpose (`@tags_with_synonyms` instead of `@synonym_target_tag_ids`)
- **Parameters**: Make parameter names explicit about what they accept (`post_or_post_id` instead of `post_id` when accepting both Post objects and IDs)
- **Methods**: Include context when it aids clarity (`update_category_read_restricted` instead of `update_read_restricted_flags`)
- **Constants**: Use descriptive names over generic ones (`NO_DESTINATION_COOKIE` instead of `NO_COOKIE`)
- **SQL aliases**: Prefer readable aliases over cryptic abbreviations (`mapped_categories` instead of `mc`)

**Example:**
```ruby
# Avoid: Generic parameter name that doesn't indicate flexibility
def reset_bumped_at(post_id = nil)
  post = post_id.is_a?(Post) ? post_id : Post.find(post_id)
end

# Prefer: Clear parameter name indicating it accepts both types
def reset_bumped_at(post_or_post_id = nil)
  post = post_or_post_id.is_a?(Post) ? post_or_post_id : Post.find(post_or_post_id)
end
```

The goal is to write code that reads like well-written prose, where the intent is immediately clear without requiring additional mental parsing or context switching.