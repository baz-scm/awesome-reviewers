---
title: Test helpers for maintainability
description: Create reusable helper methods for common testing operations to improve
  test maintainability and consistency. Design these helpers to be appropriate for
  their specific test context (integration vs system tests) and resilient to implementation
  changes.
repository: rails/rails
label: Testing
language: Other
comments_count: 2
repository_stars: 57027
---

Create reusable helper methods for common testing operations to improve test maintainability and consistency. Design these helpers to be appropriate for their specific test context (integration vs system tests) and resilient to implementation changes.

For authentication in integration tests:
```ruby
def sign_in_as(user)
  Current.session = user.sessions.create!
  
  ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|
    cookie_jar.signed[:session_id] = Current.session.id
    cookies[:session_id] = cookie_jar[:session_id]
  end
end
```

For authentication in system tests:
```ruby
def sign_in(user)
  session = user.sessions.create!
  Current.session = session
  request = ActionDispatch::Request.new(Rails.application.env_config)
  cookies = request.cookie_jar
  cookies.signed[:session_id] = { value: session.id, httponly: true, same_site: :lax }
end
```

When accessing test data, avoid hardcoding references to specific fixtures which are likely to change. Instead, use approaches that are more resilient:

```ruby
# Instead of:
test "create" do
  post passwords_path, params: { email_address: users(:one).email_address }
end

# Prefer:
setup do
  @user = User.take
end

test "create" do
  post passwords_path, params: { email_address: @user.email_address }
end
```

This approach reduces test brittleness and maintenance overhead when fixtures or underlying implementations change.
