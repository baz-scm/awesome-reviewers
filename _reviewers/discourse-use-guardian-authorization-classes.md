---
title: use Guardian authorization classes
description: Always implement authorization checks using Guardian classes rather than
  ad-hoc permission logic. Guardian classes provide a centralized, consistent approach
  to authorization that helps prevent security vulnerabilities from inconsistent or
  missing permission checks.
repository: discourse/discourse
label: Security
language: Markdown
comments_count: 1
repository_stars: 44898
---

Always implement authorization checks using Guardian classes rather than ad-hoc permission logic. Guardian classes provide a centralized, consistent approach to authorization that helps prevent security vulnerabilities from inconsistent or missing permission checks.

The main Guardian class is defined in `lib/guardian.rb`, with additional Guardian classes available in the `lib/guardian/` directory. These classes encapsulate authorization logic and should be used for all permission-related decisions in the application.

Example usage:
```ruby
# In a controller
def show
  guardian.ensure_can_see!(@topic)
  # ... rest of action
end

# In a service or model
if guardian.can_edit_post?(@post)
  # ... perform edit operation
end
```

This pattern ensures that authorization logic is:
- Centralized and maintainable
- Consistently applied across the application  
- Easier to audit for security vulnerabilities
- Following established architectural patterns

Avoid implementing custom authorization logic directly in controllers or services, as this can lead to inconsistent security enforcement and potential authorization bypass vulnerabilities.