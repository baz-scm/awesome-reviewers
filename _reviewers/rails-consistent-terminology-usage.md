---
title: Consistent terminology usage
description: Always use consistent terminology for the same concept throughout your
  codebase, documentation, and user interfaces. When multiple terms could describe
  the same thing, choose one definitive term and use it consistently everywhere.
repository: rails/rails
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 57027
---

Always use consistent terminology for the same concept throughout your codebase, documentation, and user interfaces. When multiple terms could describe the same thing, choose one definitive term and use it consistently everywhere.

For example, when referring to database configuration elements, don't alternate between calling them "configuration keys" and "connection names" - pick the most semantically accurate term (e.g., "connection name") and use it consistently:

```ruby
# GOOD:
# Connection URLs for non-primary databases can be configured using
# environment variables. The variable name is formed by concatenating the
# connection name with `_DATABASE_URL`.

# BAD:
# Similar environment variable prefixed with the configuration key...
# ...prefixed with the connection name...
# (Using inconsistent terminology for the same concept)
```

Terminology consistency reduces cognitive load for readers and maintainers, prevents confusion, and makes documentation more accessible. This principle applies equally to code comments, user-facing labels, and semantic HTML elements.
