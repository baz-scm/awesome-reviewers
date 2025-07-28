---
title: Extract complex logic
description: Break down complex methods into smaller, well-named private methods to
  improve readability and maintainability. When a method contains multiple responsibilities,
  nested conditionals, or complex logic blocks, extract these into descriptive private
  methods.
repository: mastodon/mastodon
label: Code Style
language: Ruby
comments_count: 6
repository_stars: 48691
---

Break down complex methods into smaller, well-named private methods to improve readability and maintainability. When a method contains multiple responsibilities, nested conditionals, or complex logic blocks, extract these into descriptive private methods.

This approach makes code easier to understand, test, and modify. Instead of having long methods with inline complexity, create focused methods that clearly communicate their purpose through their names.

Example of improvement:
```ruby
# Before: Complex logic inline
def require_functional!
  if current_user.functional?
    nil
  elsif !current_user.confirmed?
    redirect_to new_user_confirmation_path
  elsif current_user.pending_reconfirmation?
    redirect_to edit_user_registration_path
  else
    redirect_to edit_user_registration_path
  end
end

# After: Extracted to descriptive method
def require_functional!
  return if current_user.functional?
  redirect_to non_functional_user_setup_path
end

private

def non_functional_user_setup_path
  return new_user_confirmation_path unless current_user.confirmed?
  edit_user_registration_path
end
```

Apply this pattern when you find yourself writing complex conditional logic, data transformation blocks, or any logic that requires inline comments to explain its purpose. The extracted method name should clearly describe what the logic accomplishes.