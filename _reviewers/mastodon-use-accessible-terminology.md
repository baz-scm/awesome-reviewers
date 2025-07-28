---
title: Use accessible terminology
description: Choose clear, understandable names and terminology that are appropriate
  for your intended audience, avoiding technical jargon or obscure references that
  may not be widely understood. This is especially important for user-facing strings,
  error messages, and interface labels.
repository: mastodon/mastodon
label: Naming Conventions
language: Yaml
comments_count: 4
repository_stars: 48691
---

Choose clear, understandable names and terminology that are appropriate for your intended audience, avoiding technical jargon or obscure references that may not be widely understood. This is especially important for user-facing strings, error messages, and interface labels.

When naming user-facing elements, prioritize clarity over brevity. For example, use "Internal Notes" or "Moderator Notes" instead of ambiguous terms, and explain concepts rather than referencing technical terms like "Scunthorpe Problem" that administrators may not recognize.

Additionally, consider internationalization implications when choosing names and variable patterns. Use proper pluralization forms even for constants, as translators need context and many languages have complex pluralization rules.

Example:
```yaml
# Avoid technical jargon
comparison: Please be mindful of the Scunthorpe Problem when blocking partial matches

# Better - explain the concept clearly  
comparison: Be careful when blocking partial matches, as legitimate words may contain blocked terms

# Use proper pluralization even for constants
over_total_limit: You have exceeded the limit of %{limit} scheduled posts

# Better - supports all languages properly
over_total_limit:
  one: You have exceeded the limit of %{limit} scheduled post
  other: You have exceeded the limit of %{limit} scheduled posts
```