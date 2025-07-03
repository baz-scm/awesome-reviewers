---
title: Content security policy configuration
description: Implement Content Security Policy (CSP) configurations appropriately
  for your application's context. Use report-only mode during implementation to avoid
  breaking functionality while testing policies.
repository: rails/rails
label: Security
language: Ruby
comments_count: 4
repository_stars: 57027
---

Implement Content Security Policy (CSP) configurations appropriately for your application's context. Use report-only mode during implementation to avoid breaking functionality while testing policies.

For API endpoints, implement stricter policies:

```ruby
# In controllers serving API endpoints
content_security_policy only: :api do |policy|
  policy.default_src :none
  policy.frame_ancestors :none
  policy.sandbox        # Additional protection with minimal overhead
end
```

For user-facing pages, implement policies that balance security and functionality:

```ruby
# In application controller or specific controllers
content_security_policy do |policy|
  policy.default_src :self
  policy.script_src :self
  policy.style_src :self
  # Add sources as needed, but be as restrictive as possible
end

# Test new policies in report-only mode before enforcing
content_security_policy_report_only do |policy|
  # Configure your new policy here
  # It will be reported but not enforced
end
```

Always prefer hash or nonce-based source validation over 'unsafe-inline' when script execution from inline elements is required. Remove unnecessary CSP configurations to avoid confusion and maintain clean security controls.
