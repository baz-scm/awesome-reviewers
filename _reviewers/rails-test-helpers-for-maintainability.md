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


[
  {
    "discussion_id": "1921578313",
    "pr_number": 53708,
    "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
    "created_at": "2025-01-19T15:24:41+00:00",
    "commented_code": "module SessionTestHelper\n  def sign_in_as(user)\n    Current.session = user.sessions.create!\n\n    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n      cookie_jar.signed[:session_id] = Current.session.id\n      cookies[:session_id] = cookie_jar[:session_id]",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1921578313",
        "repo_full_name": "rails/rails",
        "pr_number": 53708,
        "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
        "discussion_id": "1921578313",
        "commented_code": "@@ -0,0 +1,15 @@\n+module SessionTestHelper\n+  def sign_in_as(user)\n+    Current.session = user.sessions.create!\n+\n+    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n+      cookie_jar.signed[:session_id] = Current.session.id\n+      cookies[:session_id] = cookie_jar[:session_id]",
        "comment_created_at": "2025-01-19T15:24:41+00:00",
        "comment_author": "MatheusRich",
        "comment_body": "Is this supposed to be added o system tests or request tests? I don't remember if system tests can access cookies ",
        "pr_file_module": null
      },
      {
        "comment_id": "1922020882",
        "repo_full_name": "rails/rails",
        "pr_number": 53708,
        "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
        "discussion_id": "1921578313",
        "commented_code": "@@ -0,0 +1,15 @@\n+module SessionTestHelper\n+  def sign_in_as(user)\n+    Current.session = user.sessions.create!\n+\n+    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n+      cookie_jar.signed[:session_id] = Current.session.id\n+      cookies[:session_id] = cookie_jar[:session_id]",
        "comment_created_at": "2025-01-20T08:56:31+00:00",
        "comment_author": "gobijan",
        "comment_body": "This is for IntegrationTests (ActionDispatch::IntegrationTest).",
        "pr_file_module": null
      },
      {
        "comment_id": "1922650053",
        "repo_full_name": "rails/rails",
        "pr_number": 53708,
        "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
        "discussion_id": "1921578313",
        "commented_code": "@@ -0,0 +1,15 @@\n+module SessionTestHelper\n+  def sign_in_as(user)\n+    Current.session = user.sessions.create!\n+\n+    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n+      cookie_jar.signed[:session_id] = Current.session.id\n+      cookies[:session_id] = cookie_jar[:session_id]",
        "comment_created_at": "2025-01-20T16:35:14+00:00",
        "comment_author": "MatheusRich",
        "comment_body": "Should we have one for system tests too? I know @dhh is not a big fan of them, but for smoke tests, a set of system tests are useful. Should we let that for each app to implement? Maybe a initial implementation on the docs could be an alternative, if we don't want to ship it in the framework.",
        "pr_file_module": null
      },
      {
        "comment_id": "1922736589",
        "repo_full_name": "rails/rails",
        "pr_number": 53708,
        "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
        "discussion_id": "1921578313",
        "commented_code": "@@ -0,0 +1,15 @@\n+module SessionTestHelper\n+  def sign_in_as(user)\n+    Current.session = user.sessions.create!\n+\n+    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n+      cookie_jar.signed[:session_id] = Current.session.id\n+      cookies[:session_id] = cookie_jar[:session_id]",
        "comment_created_at": "2025-01-20T18:08:01+00:00",
        "comment_author": "gobijan",
        "comment_body": "Well good question. I think system tests are probably way simpler. These helpers here were not trivial because of the cookie jar problem mentioned in the referenced discussion.\r\n\r\nFor system tests it's pretty straightforward I guess. Something like:\r\n\r\n```\r\nvisit new_session_url\r\nfill_in \"Email\", with: \"test@example.com\"\r\nfill_in \"Password\", with: \"password123\"\r\nclick_on \"Sign in\"\r\n```\r\n\r\nWhere should logic for this go? Directly in the ApplicationSystemTestCase class?\r\nAnyways I needed the IntegrationTest functionality as I was repeating it in all my projects. I let you guys decide how to move forward.",
        "pr_file_module": null
      },
      {
        "comment_id": "1922786344",
        "repo_full_name": "rails/rails",
        "pr_number": 53708,
        "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
        "discussion_id": "1921578313",
        "commented_code": "@@ -0,0 +1,15 @@\n+module SessionTestHelper\n+  def sign_in_as(user)\n+    Current.session = user.sessions.create!\n+\n+    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n+      cookie_jar.signed[:session_id] = Current.session.id\n+      cookies[:session_id] = cookie_jar[:session_id]",
        "comment_created_at": "2025-01-20T19:25:07+00:00",
        "comment_author": "MatheusRich",
        "comment_body": "I wonder if the system specs should actually login, or set cookies more \"manually\" too.\r\n\r\nI'll defer to @dhh to say if this is necessary or not. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1964111180",
        "repo_full_name": "rails/rails",
        "pr_number": 53708,
        "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
        "discussion_id": "1921578313",
        "commented_code": "@@ -0,0 +1,15 @@\n+module SessionTestHelper\n+  def sign_in_as(user)\n+    Current.session = user.sessions.create!\n+\n+    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n+      cookie_jar.signed[:session_id] = Current.session.id\n+      cookies[:session_id] = cookie_jar[:session_id]",
        "comment_created_at": "2025-02-20T18:06:49+00:00",
        "comment_author": "csculley",
        "comment_body": "For system tests, I needed to add in the following to get that solution to work:\r\n```\r\npage.instance_variable_set(:@touched, false)\r\npage.reset!\r\n```\r\nHowever, this is pretty hacky, and I'm pretty sure there's a better solution for system tests",
        "pr_file_module": null
      },
      {
        "comment_id": "1964116185",
        "repo_full_name": "rails/rails",
        "pr_number": 53708,
        "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
        "discussion_id": "1921578313",
        "commented_code": "@@ -0,0 +1,15 @@\n+module SessionTestHelper\n+  def sign_in_as(user)\n+    Current.session = user.sessions.create!\n+\n+    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n+      cookie_jar.signed[:session_id] = Current.session.id\n+      cookies[:session_id] = cookie_jar[:session_id]",
        "comment_created_at": "2025-02-20T18:10:44+00:00",
        "comment_author": "MatheusRich",
        "comment_body": "I had something created for system specs before this PR:\r\n\r\n```rb\r\n    def sign_in(user = users(:john))\r\n      session = user.sessions.create!\r\n      Current.session = session\r\n      request = ActionDispatch::Request.new(Rails.application.env_config)\r\n      cookies = request.cookie_jar\r\n      cookies.signed[:session_id] = { value: session.id, httponly: true, same_site: :lax }\r\n    end\r\n```\r\n\r\nHope that helps",
        "pr_file_module": null
      },
      {
        "comment_id": "1964119286",
        "repo_full_name": "rails/rails",
        "pr_number": 53708,
        "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
        "discussion_id": "1921578313",
        "commented_code": "@@ -0,0 +1,15 @@\n+module SessionTestHelper\n+  def sign_in_as(user)\n+    Current.session = user.sessions.create!\n+\n+    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n+      cookie_jar.signed[:session_id] = Current.session.id\n+      cookies[:session_id] = cookie_jar[:session_id]",
        "comment_created_at": "2025-02-20T18:13:04+00:00",
        "comment_author": "csculley",
        "comment_body": "Just an update, the solution in https://github.com/rails/rails/issues/53207#issuecomment-2628448719 works better for me than the page resetting! I think there was a significant amount of flake introduced by using stock capybara fill_in to initiate the session",
        "pr_file_module": null
      },
      {
        "comment_id": "1964131999",
        "repo_full_name": "rails/rails",
        "pr_number": 53708,
        "pr_file": "railties/lib/rails/generators/rails/authentication/templates/test/helpers/session_test_helper.rb.tt",
        "discussion_id": "1921578313",
        "commented_code": "@@ -0,0 +1,15 @@\n+module SessionTestHelper\n+  def sign_in_as(user)\n+    Current.session = user.sessions.create!\n+\n+    ActionDispatch::TestRequest.create.cookie_jar.tap do |cookie_jar|\n+      cookie_jar.signed[:session_id] = Current.session.id\n+      cookies[:session_id] = cookie_jar[:session_id]",
        "comment_created_at": "2025-02-20T18:22:47+00:00",
        "comment_author": "csculley",
        "comment_body": "Hah, @MatheusRich, your comment didn't seem to load for me in time, but I think we came to the same conclusion :smile: ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1973680913",
    "pr_number": 53255,
    "pr_file": "railties/lib/rails/generators/test_unit/authentication/templates/test/controllers/passwords_controller_test.rb.tt",
    "created_at": "2025-02-27T14:23:02+00:00",
    "commented_code": "require \"test_helper\"\n\nclass PasswordsControllerTest < ActionDispatch::IntegrationTest\n  test \"new\" do\n    get new_password_path\n    \n    assert_response :success\n  end\n\n  test \"create\" do\n    post passwords_path, params: { email_address: users(:one).email_address }",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1973680913",
        "repo_full_name": "rails/rails",
        "pr_number": 53255,
        "pr_file": "railties/lib/rails/generators/test_unit/authentication/templates/test/controllers/passwords_controller_test.rb.tt",
        "discussion_id": "1973680913",
        "commented_code": "@@ -0,0 +1,66 @@\n+require \"test_helper\"\n+\n+class PasswordsControllerTest < ActionDispatch::IntegrationTest\n+  test \"new\" do\n+    get new_password_path\n+    \n+    assert_response :success\n+  end\n+\n+  test \"create\" do\n+    post passwords_path, params: { email_address: users(:one).email_address }",
        "comment_created_at": "2025-02-27T14:23:02+00:00",
        "comment_author": "dhh",
        "comment_body": "Don't like hardcoding this to the stock fixtures, because they're so likely to change, and then it's a lot of busywork to update. What we could do instead is something like `User.take`, which will grab a random user to do this with.",
        "pr_file_module": null
      },
      {
        "comment_id": "1976708275",
        "repo_full_name": "rails/rails",
        "pr_number": 53255,
        "pr_file": "railties/lib/rails/generators/test_unit/authentication/templates/test/controllers/passwords_controller_test.rb.tt",
        "discussion_id": "1973680913",
        "commented_code": "@@ -0,0 +1,66 @@\n+require \"test_helper\"\n+\n+class PasswordsControllerTest < ActionDispatch::IntegrationTest\n+  test \"new\" do\n+    get new_password_path\n+    \n+    assert_response :success\n+  end\n+\n+  test \"create\" do\n+    post passwords_path, params: { email_address: users(:one).email_address }",
        "comment_created_at": "2025-03-02T20:23:39+00:00",
        "comment_author": "codergeek121",
        "comment_body": "I rebased and updated the test according to your suggestion. Instead of relying on the `:one` fixture, I'm using `User.take` in a `setup` now instead \ud83d\udc4d",
        "pr_file_module": null
      }
    ]
  }
]
