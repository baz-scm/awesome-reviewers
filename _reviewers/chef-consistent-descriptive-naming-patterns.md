---
title: Consistent descriptive naming patterns
description: 'Use clear, descriptive names that follow consistent patterns across
  the codebase. For methods and properties:


  1. Use intention-revealing names that clearly indicate purpose'
repository: chef/chef
label: Naming Conventions
language: Ruby
comments_count: 7
repository_stars: 7860
---

Use clear, descriptive names that follow consistent patterns across the codebase. For methods and properties:

1. Use intention-revealing names that clearly indicate purpose
2. For boolean methods, use question-mark suffixes and appropriate prefixes
3. Maintain consistent naming patterns across similar properties
4. Use lowercase for variables unless they are true constants

Examples:
```ruby
# Poor naming
def compare_users  # unclear if returns boolean
def detect_certificate_key  # verb is ambiguous
property :certpassword  # inconsistent with other properties

# Good naming
def users_changed?  # clear boolean return
def certificate_key_exist?  # clear boolean check
property :cert_password  # consistent with other properties

# Property naming consistency
property :user      # preferred over user_name
property :password  # preferred over pass
```

This pattern improves code readability, maintains consistency, and reduces cognitive load when working across different parts of the codebase.
