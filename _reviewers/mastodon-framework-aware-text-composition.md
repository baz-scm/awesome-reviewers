---
title: Framework-aware text composition
description: When writing user-facing text (error messages, notifications, labels),
  understand how your framework automatically processes and modifies that text before
  it reaches users. Many frameworks like Rails automatically combine messages with
  attribute names or apply other transformations that can result in redundant or grammatically
  incorrect output.
repository: mastodon/mastodon
label: Documentation
language: Yaml
comments_count: 2
repository_stars: 48691
---

When writing user-facing text (error messages, notifications, labels), understand how your framework automatically processes and modifies that text before it reaches users. Many frameworks like Rails automatically combine messages with attribute names or apply other transformations that can result in redundant or grammatically incorrect output.

Before finalizing any user-facing text, consider:
- How the framework will process or modify your text
- Different contexts in which the message might appear (past vs future events, different user states)
- Whether automatic prefixes or suffixes will create redundant phrasing

Example from Rails localization:
```yaml
# Problematic - Rails prefixes with "Fields"
errors:
  fields_with_values_missing_names: Names of extra profile fields with values cannot be empty
# Result: "Fields Names of extra profile fields..."

# Better - Account for Rails' automatic prefixing
errors:
  fields_with_values_missing_names: with values cannot have empty names
# Result: "Fields with values cannot have empty names"
```

Always test your messages in their actual runtime context to ensure they read naturally and provide clear guidance to users.