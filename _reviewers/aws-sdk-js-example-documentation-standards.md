---
title: Example documentation standards
description: Organize API documentation examples for maximum clarity and usefulness.
  Place hand-written examples before generated examples since they're typically more
  valuable to users. When using @example tags, include only the descriptive title
  without redundant 'Example:' prefixes.
repository: aws/aws-sdk-js
label: Documentation
language: Ruby
comments_count: 2
repository_stars: 7628
---

Organize API documentation examples for maximum clarity and usefulness. Place hand-written examples before generated examples since they're typically more valuable to users. When using @example tags, include only the descriptive title without redundant 'Example:' prefixes.

For instance:
```ruby
# Good
@example Custom implementation
  # Hand-written example here
@example Calling the operation
  # Generated example here

# Avoid
@example Example: Custom implementation
  # Example here
```

This approach improves readability and maintains consistent documentation style.
