---
title: verify authorization explicitly
description: Always perform explicit authorization checks rather than assuming existing
  security controls are sufficient. Security vulnerabilities often arise from bypassed
  or missing permission verification, especially in edge cases like impersonation
  windows, controller action bypasses, or privilege escalation scenarios.
repository: discourse/discourse
label: Security
language: Ruby
comments_count: 8
repository_stars: 44898
---

Always perform explicit authorization checks rather than assuming existing security controls are sufficient. Security vulnerabilities often arise from bypassed or missing permission verification, especially in edge cases like impersonation windows, controller action bypasses, or privilege escalation scenarios.

Key practices:
- Add explicit permission checks even when controller-level security exists
- Verify user capabilities at the method level, not just at routing
- Handle edge cases like time windows where permissions might change
- Ensure anonymous users are properly restricted from authenticated features

Example from impersonation security:
```ruby
def impersonated_user
  return if impersonated_user_id.blank?
  return if impersonation_expires_at.blank? || impersonation_expires_at.past?
  
  # Add explicit guardian check for edge cases
  return unless Guardian.new(user).can_impersonate?(target_user)
  
  User.find_by(id: impersonated_user_id).tap { |u| u.is_impersonating = true }
end
```

Example from permission methods:
```ruby
def can_create_theme?(user)
  return false if !user.admin?  # Explicit check first
  # Additional restrictions can be applied via modifiers
  DiscoursePluginRegistry.apply_modifier(:user_guardian_can_create_theme, true, user, self)
end
```

This prevents security bypasses that occur when relying solely on higher-level controls that may not cover all code paths or edge cases.