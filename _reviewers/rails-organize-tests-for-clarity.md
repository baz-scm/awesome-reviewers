---
title: Organize tests for clarity
description: 'Structure tests to maximize clarity and maintainability by:

  1. Placing related tests together in appropriate test files

  2. Using built-in assertion helpers instead of raw assertions'
repository: rails/rails
label: Testing
language: Ruby
comments_count: 8
repository_stars: 57027
---

Structure tests to maximize clarity and maintainability by:
1. Placing related tests together in appropriate test files
2. Using built-in assertion helpers instead of raw assertions
3. Extracting common test helpers when patterns emerge
4. Preferring fixtures over hardcoded values for test data

Example of applying these principles:

```ruby
# Bad
def test_content_changes
  message = Message.create!(content: "Hello")
  message.content = ""
  message.save
  assert_equal 0, message.content.embeds.count
end

# Good
def test_content_changes
  message = messages(:greeting)  # Use fixture
  assert_changes -> { message.content.embeds.count }, from: 1, to: 0 do
    message.update!(content: "")
  end
end

# Extract shared assertions into helpers when pattern emerges
def assert_content_embeds_change(message, from:, to:, &block)
  assert_changes -> { message.content.embeds.count }, from: from, to: to, &block
end
```


[
  {
    "discussion_id": "1485398764",
    "pr_number": 51045,
    "pr_file": "activerecord/test/cases/relation/distinct_test.rb",
    "created_at": "2024-02-11T01:02:43+00:00",
    "commented_code": "# frozen_string_literal: true",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1485398764",
        "repo_full_name": "rails/rails",
        "pr_number": 51045,
        "pr_file": "activerecord/test/cases/relation/distinct_test.rb",
        "discussion_id": "1485398764",
        "commented_code": "@@ -0,0 +1,27 @@\n+# frozen_string_literal: true",
        "comment_created_at": "2024-02-11T01:02:43+00:00",
        "comment_author": "fatkodima",
        "comment_body": "I think there is no need to create a separate test class for this - can be placed in one of the existing ones.",
        "pr_file_module": null
      },
      {
        "comment_id": "1485399890",
        "repo_full_name": "rails/rails",
        "pr_number": 51045,
        "pr_file": "activerecord/test/cases/relation/distinct_test.rb",
        "discussion_id": "1485398764",
        "commented_code": "@@ -0,0 +1,27 @@\n+# frozen_string_literal: true",
        "comment_created_at": "2024-02-11T01:05:53+00:00",
        "comment_author": "joshuay03",
        "comment_body": "I couldn't find a single suite for query methods (nor any that are specifically for `#distinct`). And since there are classes like these:\r\n\r\n- https://github.com/rails/rails/blob/main/activerecord/test/cases/relation/merging_test.rb\r\n- https://github.com/rails/rails/blob/main/activerecord/test/cases/excluding_test.rb\r\n\r\nI opted to create a separate one. Which existing class do you think would be the most appropriate instead?",
        "pr_file_module": null
      },
      {
        "comment_id": "1485564440",
        "repo_full_name": "rails/rails",
        "pr_number": 51045,
        "pr_file": "activerecord/test/cases/relation/distinct_test.rb",
        "discussion_id": "1485398764",
        "commented_code": "@@ -0,0 +1,27 @@\n+# frozen_string_literal: true",
        "comment_created_at": "2024-02-11T10:15:28+00:00",
        "comment_author": "fatkodima",
        "comment_body": "I think it can be placed after https://github.com/rails/rails/blob/0f9aaa5ca9b8421ebf42b3d7720632d4c1cae5fc/activerecord/test/cases/relations_test.rb#L1782\r\n\r\nAnd for `distinct.count`, there are lots of tests in `calculations_test.rb`. So I would left only the second test and made it simpler - no need to use associations/where/etc, a simple\r\n```ruby\r\nassert_raises(..., match: ...) do\r\n  Post.distinct(\"not_true\")\r\nend\r\n```\r\nwould be enough.",
        "pr_file_module": null
      },
      {
        "comment_id": "1485568053",
        "repo_full_name": "rails/rails",
        "pr_number": 51045,
        "pr_file": "activerecord/test/cases/relation/distinct_test.rb",
        "discussion_id": "1485398764",
        "commented_code": "@@ -0,0 +1,27 @@\n+# frozen_string_literal: true",
        "comment_created_at": "2024-02-11T10:39:35+00:00",
        "comment_author": "joshuay03",
        "comment_body": "I've moved the test to where you suggested and simplified it.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "120422175",
    "pr_number": 28887,
    "pr_file": "activerecord/test/cases/errors_test.rb",
    "created_at": "2017-06-06T17:13:13+00:00",
    "commented_code": "end\n    end\n  end\n\n  def test_association_errors_copied_to_foreign_key",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "120422175",
        "repo_full_name": "rails/rails",
        "pr_number": 28887,
        "pr_file": "activerecord/test/cases/errors_test.rb",
        "discussion_id": "120422175",
        "commented_code": "@@ -13,4 +15,19 @@ def test_can_be_instantiated_with_no_args\n       end\n     end\n   end\n+\n+  def test_association_errors_copied_to_foreign_key",
        "comment_created_at": "2017-06-06T17:13:13+00:00",
        "comment_author": "robin850",
        "comment_body": "That's certainly not the right place to put such test. You can move it to `validations_test.rb`.",
        "pr_file_module": null
      },
      {
        "comment_id": "120481132",
        "repo_full_name": "rails/rails",
        "pr_number": 28887,
        "pr_file": "activerecord/test/cases/errors_test.rb",
        "discussion_id": "120422175",
        "commented_code": "@@ -13,4 +15,19 @@ def test_can_be_instantiated_with_no_args\n       end\n     end\n   end\n+\n+  def test_association_errors_copied_to_foreign_key",
        "comment_created_at": "2017-06-06T21:08:41+00:00",
        "comment_author": "edwardmp",
        "comment_body": "Personally I don't think validations_test is the right place for it, as the logic relates more to errors itself than validations, but it's your call so I will modify it to reflect your requested changes.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2121932598",
    "pr_number": 55127,
    "pr_file": "activejob/test/jobs/continuable_duplicate_step_job.rb",
    "created_at": "2025-06-02T18:56:21+00:00",
    "commented_code": "# frozen_string_literal: true\n\nclass ContinuableDuplicateStepJob < ActiveJob::Base\n  include ActiveJob::Continuable\n\n  def perform\n    step :duplicate do |step|\n    end\n    step :duplicate do |step|\n    end\n  end\nend",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2121932598",
        "repo_full_name": "rails/rails",
        "pr_number": 55127,
        "pr_file": "activejob/test/jobs/continuable_duplicate_step_job.rb",
        "discussion_id": "2121932598",
        "commented_code": "@@ -0,0 +1,12 @@\n+# frozen_string_literal: true\n+\n+class ContinuableDuplicateStepJob < ActiveJob::Base\n+  include ActiveJob::Continuable\n+\n+  def perform\n+    step :duplicate do |step|\n+    end\n+    step :duplicate do |step|\n+    end\n+  end\n+end",
        "comment_created_at": "2025-06-02T18:56:21+00:00",
        "comment_author": "byroot",
        "comment_body": "All these \"fixture\" jobs could be defined inside the test classes themselves. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2123029782",
        "repo_full_name": "rails/rails",
        "pr_number": 55127,
        "pr_file": "activejob/test/jobs/continuable_duplicate_step_job.rb",
        "discussion_id": "2121932598",
        "commented_code": "@@ -0,0 +1,12 @@\n+# frozen_string_literal: true\n+\n+class ContinuableDuplicateStepJob < ActiveJob::Base\n+  include ActiveJob::Continuable\n+\n+  def perform\n+    step :duplicate do |step|\n+    end\n+    step :duplicate do |step|\n+    end\n+  end\n+end",
        "comment_created_at": "2025-06-03T07:52:36+00:00",
        "comment_author": "djmb",
        "comment_body": "There are a couple of test jobs defined in their classes, but the pattern here is separate files even though most jobs are only used by one test case. But either way works for me if you'd prefer I moved them.",
        "pr_file_module": null
      },
      {
        "comment_id": "2123366550",
        "repo_full_name": "rails/rails",
        "pr_number": 55127,
        "pr_file": "activejob/test/jobs/continuable_duplicate_step_job.rb",
        "discussion_id": "2121932598",
        "commented_code": "@@ -0,0 +1,12 @@\n+# frozen_string_literal: true\n+\n+class ContinuableDuplicateStepJob < ActiveJob::Base\n+  include ActiveJob::Continuable\n+\n+  def perform\n+    step :duplicate do |step|\n+    end\n+    step :duplicate do |step|\n+    end\n+  end\n+end",
        "comment_created_at": "2025-06-03T10:13:57+00:00",
        "comment_author": "byroot",
        "comment_body": "Thanks. IMHO it's much easier to understand tests when the job they rely on is just above.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2094782011",
    "pr_number": 51291,
    "pr_file": "actiontext/test/unit/model_test.rb",
    "created_at": "2025-05-19T03:38:46+00:00",
    "commented_code": "assert_equal blob, embeds.first.blob\n  end\n\n  test \"saving empty content empties the embeds\" do\n    blob = create_file_blob(filename: \"racecar.jpg\", content_type: \"image/jpeg\")\n    message = Message.create!(subject: \"Greetings\", content: ActionText::Content.new(\"Hello world\").append_attachables(blob))\n    assert message.content.embeds.sole\n\n    message.content = \"\"\n    message.save\n\n    assert_empty message.content.embeds",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2094782011",
        "repo_full_name": "rails/rails",
        "pr_number": 51291,
        "pr_file": "actiontext/test/unit/model_test.rb",
        "discussion_id": "2094782011",
        "commented_code": "@@ -76,6 +76,28 @@ class ActionText::ModelTest < ActiveSupport::TestCase\n     assert_equal blob, embeds.first.blob\n   end\n \n+  test \"saving empty content empties the embeds\" do\n+    blob = create_file_blob(filename: \"racecar.jpg\", content_type: \"image/jpeg\")\n+    message = Message.create!(subject: \"Greetings\", content: ActionText::Content.new(\"Hello world\").append_attachables(blob))\n+    assert message.content.embeds.sole\n+\n+    message.content = \"\"\n+    message.save\n+\n+    assert_empty message.content.embeds",
        "comment_created_at": "2025-05-19T03:38:46+00:00",
        "comment_author": "seanpdoyle",
        "comment_body": "Have you considered combining these separate assertions into a single [assert_changes](https://edgeapi.rubyonrails.org/classes/ActiveSupport/Testing/Assertions.html#method-i-assert_changes) call?\r\n\r\n```suggestion\r\n    assert_changes -> { message.content.embeds.count }, from: 1, to: 0 do\r\n      message.update!(content: \"\")\r\n    end\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2094873615",
        "repo_full_name": "rails/rails",
        "pr_number": 51291,
        "pr_file": "actiontext/test/unit/model_test.rb",
        "discussion_id": "2094782011",
        "commented_code": "@@ -76,6 +76,28 @@ class ActionText::ModelTest < ActiveSupport::TestCase\n     assert_equal blob, embeds.first.blob\n   end\n \n+  test \"saving empty content empties the embeds\" do\n+    blob = create_file_blob(filename: \"racecar.jpg\", content_type: \"image/jpeg\")\n+    message = Message.create!(subject: \"Greetings\", content: ActionText::Content.new(\"Hello world\").append_attachables(blob))\n+    assert message.content.embeds.sole\n+\n+    message.content = \"\"\n+    message.save\n+\n+    assert_empty message.content.embeds",
        "comment_created_at": "2025-05-19T05:40:56+00:00",
        "comment_author": "JoeDupuis",
        "comment_body": "Thank you! Much cleaner!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1769638448",
    "pr_number": 53007,
    "pr_file": "activerecord/test/cases/associations_test.rb",
    "created_at": "2024-09-21T18:55:43+00:00",
    "commented_code": "assert_equal(expected_comments.sort, comments.sort)\n  end\n\n  def test_foreign_key_is_in_ignored_columns\n    assert_raises ArgumentError do",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1769638448",
        "repo_full_name": "rails/rails",
        "pr_number": 53007,
        "pr_file": "activerecord/test/cases/associations_test.rb",
        "discussion_id": "1769638448",
        "commented_code": "@@ -241,6 +241,17 @@ def test_has_many_association_from_a_model_with_query_constraints_different_from\n     assert_equal(expected_comments.sort, comments.sort)\n   end\n \n+  def test_foreign_key_is_in_ignored_columns\n+    assert_raises ArgumentError do",
        "comment_created_at": "2024-09-21T18:55:43+00:00",
        "comment_author": "p8",
        "comment_body": "You can use `match` to assert to expected ArgumentError is raised:\r\n```suggestion\r\n    assert_raises ArgumentError, match: /the column post_id is ignored/ do\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2050721822",
    "pr_number": 54938,
    "pr_file": "actionpack/lib/action_dispatch/testing/assertions/response.rb",
    "created_at": "2025-04-18T14:40:18+00:00",
    "commented_code": "assert_operator redirect_expected, :===, redirect_is, message\n      end\n\n      # Asserts that the given +text+ is present somewhere in the response body.\n      #\n      #     assert_in_body fixture(:name).description\n      def assert_in_body(text)\n        assert_match(/#{text}/, @response.body)",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2050721822",
        "repo_full_name": "rails/rails",
        "pr_number": 54938,
        "pr_file": "actionpack/lib/action_dispatch/testing/assertions/response.rb",
        "discussion_id": "2050721822",
        "commented_code": "@@ -71,6 +71,20 @@ def assert_redirected_to(url_options = {}, options = {}, message = nil)\n         assert_operator redirect_expected, :===, redirect_is, message\n       end\n \n+      # Asserts that the given +text+ is present somewhere in the response body.\n+      #\n+      #     assert_in_body fixture(:name).description\n+      def assert_in_body(text)\n+        assert_match(/#{text}/, @response.body)",
        "comment_created_at": "2025-04-18T14:40:18+00:00",
        "comment_author": "Edouard-chin",
        "comment_body": "Maybe we can escape the Regexp? I can see people using something like `assert_in_body(\"Name (optional)\")` which wouldn't match because of the unescaped parenthesis.",
        "pr_file_module": null
      },
      {
        "comment_id": "2050729423",
        "repo_full_name": "rails/rails",
        "pr_number": 54938,
        "pr_file": "actionpack/lib/action_dispatch/testing/assertions/response.rb",
        "discussion_id": "2050721822",
        "commented_code": "@@ -71,6 +71,20 @@ def assert_redirected_to(url_options = {}, options = {}, message = nil)\n         assert_operator redirect_expected, :===, redirect_is, message\n       end\n \n+      # Asserts that the given +text+ is present somewhere in the response body.\n+      #\n+      #     assert_in_body fixture(:name).description\n+      def assert_in_body(text)\n+        assert_match(/#{text}/, @response.body)",
        "comment_created_at": "2025-04-18T14:45:19+00:00",
        "comment_author": "dhh",
        "comment_body": "Good idea \ud83d\udc4d",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "592444784",
    "pr_number": 41659,
    "pr_file": "actiontext/test/unit/model_encryption_test.rb",
    "created_at": "2021-03-11T15:13:59+00:00",
    "commented_code": "# frozen_string_literal: true\n\nrequire \"test_helper\"\n\nclass ActionText::ModelEncryptionTest < ActiveSupport::TestCase\n  test \"encrypt content based on :encrypted option at declaration time\" do\n    encrypted_message = EncryptedMessage.create!(subject: \"Greetings\", content: \"Hey there\")\n    assert_encrypted_rich_text_attribute encrypted_message, :content, \"Hey there\"\n\n    clear_message = Message.create!(subject: \"Greetings\", content: \"Hey there\")\n    assert_not_encrypted_rich_text_attribute clear_message, :content, \"Hey there\"\n  end\n\n  test \"include rich text attributes when encrypting the model\" do\n    content = \"<p>the space force is here, we are safe now!</p>\"\n\n    message = ActiveRecord::Encryption.without_encryption do\n      EncryptedMessage.create!(subject: \"Greetings\", content: content)\n    end\n\n    message.encrypt\n\n    assert_encrypted_rich_text_attribute(message, :content, content)\n  end\n\n  test \"encrypts lets you skip rich texts when encrypting\" do\n    content = \"<p>the space force is here, we are safe now!</p>\"\n\n    message = ActiveRecord::Encryption.without_encryption do\n      EncryptedMessage.create!(subject: \"Greetings\", content: content)\n    end\n\n    message.encrypt(skip_rich_texts: true)\n\n    assert_not_encrypted_rich_text_attribute(message, :content, content)\n  end\n\n  private\n    def assert_encrypted_rich_text_attribute(model, attribute_name, expected_value)",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "592444784",
        "repo_full_name": "rails/rails",
        "pr_number": 41659,
        "pr_file": "actiontext/test/unit/model_encryption_test.rb",
        "discussion_id": "592444784",
        "commented_code": "@@ -0,0 +1,48 @@\n+# frozen_string_literal: true\n+\n+require \"test_helper\"\n+\n+class ActionText::ModelEncryptionTest < ActiveSupport::TestCase\n+  test \"encrypt content based on :encrypted option at declaration time\" do\n+    encrypted_message = EncryptedMessage.create!(subject: \"Greetings\", content: \"Hey there\")\n+    assert_encrypted_rich_text_attribute encrypted_message, :content, \"Hey there\"\n+\n+    clear_message = Message.create!(subject: \"Greetings\", content: \"Hey there\")\n+    assert_not_encrypted_rich_text_attribute clear_message, :content, \"Hey there\"\n+  end\n+\n+  test \"include rich text attributes when encrypting the model\" do\n+    content = \"<p>the space force is here, we are safe now!</p>\"\n+\n+    message = ActiveRecord::Encryption.without_encryption do\n+      EncryptedMessage.create!(subject: \"Greetings\", content: content)\n+    end\n+\n+    message.encrypt\n+\n+    assert_encrypted_rich_text_attribute(message, :content, content)\n+  end\n+\n+  test \"encrypts lets you skip rich texts when encrypting\" do\n+    content = \"<p>the space force is here, we are safe now!</p>\"\n+\n+    message = ActiveRecord::Encryption.without_encryption do\n+      EncryptedMessage.create!(subject: \"Greetings\", content: content)\n+    end\n+\n+    message.encrypt(skip_rich_texts: true)\n+\n+    assert_not_encrypted_rich_text_attribute(message, :content, content)\n+  end\n+\n+  private\n+    def assert_encrypted_rich_text_attribute(model, attribute_name, expected_value)",
        "comment_created_at": "2021-03-11T15:13:59+00:00",
        "comment_author": "seanpdoyle",
        "comment_body": "Could some form of these two helpers be extracted into a consumer-facing module, so that similar assertions could be made from application test suites?",
        "pr_file_module": null
      },
      {
        "comment_id": "592483503",
        "repo_full_name": "rails/rails",
        "pr_number": 41659,
        "pr_file": "actiontext/test/unit/model_encryption_test.rb",
        "discussion_id": "592444784",
        "commented_code": "@@ -0,0 +1,48 @@\n+# frozen_string_literal: true\n+\n+require \"test_helper\"\n+\n+class ActionText::ModelEncryptionTest < ActiveSupport::TestCase\n+  test \"encrypt content based on :encrypted option at declaration time\" do\n+    encrypted_message = EncryptedMessage.create!(subject: \"Greetings\", content: \"Hey there\")\n+    assert_encrypted_rich_text_attribute encrypted_message, :content, \"Hey there\"\n+\n+    clear_message = Message.create!(subject: \"Greetings\", content: \"Hey there\")\n+    assert_not_encrypted_rich_text_attribute clear_message, :content, \"Hey there\"\n+  end\n+\n+  test \"include rich text attributes when encrypting the model\" do\n+    content = \"<p>the space force is here, we are safe now!</p>\"\n+\n+    message = ActiveRecord::Encryption.without_encryption do\n+      EncryptedMessage.create!(subject: \"Greetings\", content: content)\n+    end\n+\n+    message.encrypt\n+\n+    assert_encrypted_rich_text_attribute(message, :content, content)\n+  end\n+\n+  test \"encrypts lets you skip rich texts when encrypting\" do\n+    content = \"<p>the space force is here, we are safe now!</p>\"\n+\n+    message = ActiveRecord::Encryption.without_encryption do\n+      EncryptedMessage.create!(subject: \"Greetings\", content: content)\n+    end\n+\n+    message.encrypt(skip_rich_texts: true)\n+\n+    assert_not_encrypted_rich_text_attribute(message, :content, content)\n+  end\n+\n+  private\n+    def assert_encrypted_rich_text_attribute(model, attribute_name, expected_value)",
        "comment_created_at": "2021-03-11T15:57:13+00:00",
        "comment_author": "jorgemanrubia",
        "comment_body": "Yes @seanpdoyle I think that makes a lot of sense sense. Most people shouldn't need those, but if you are building a system to mass-encrypt (or re-encrypt) data, those would be very useful \ud83d\udc4d. Not sure is I'll get to it in this PR but, if not, it's a great candidate for a future iteration.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1982842029",
    "pr_number": 53726,
    "pr_file": "railties/lib/rails/generators/test_unit/authentication/templates/test/controllers/sessions_controller_test.rb",
    "created_at": "2025-03-06T07:41:36+00:00",
    "commented_code": "require \"test_helper\"\n\nclass SessionsControllerTest < ActionDispatch::IntegrationTest\n  test \"new\" do\n    get new_session_url\n    assert_response :success\n  end\n\n  test \"create with valid credentials\" do\n    post session_url, params: { email_address: \"one@example.com\", password: \"password\" }",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1982842029",
        "repo_full_name": "rails/rails",
        "pr_number": 53726,
        "pr_file": "railties/lib/rails/generators/test_unit/authentication/templates/test/controllers/sessions_controller_test.rb",
        "discussion_id": "1982842029",
        "commented_code": "@@ -0,0 +1,31 @@\n+require \"test_helper\"\n+\n+class SessionsControllerTest < ActionDispatch::IntegrationTest\n+  test \"new\" do\n+    get new_session_url\n+    assert_response :success\n+  end\n+\n+  test \"create with valid credentials\" do\n+    post session_url, params: { email_address: \"one@example.com\", password: \"password\" }",
        "comment_created_at": "2025-03-06T07:41:36+00:00",
        "comment_author": "jeromedalbert",
        "comment_body": "I left `\"one@example.com\"` hardcoded since `\"password\"` needs to be hardcoded anyways, but if needed I am happy to do something like `setup { @user = User.take }` with the following:\r\n\r\n```ruby\r\n    post session_url, params: { email_address: @user.email_address, password: \"password\" }\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1985118984",
        "repo_full_name": "rails/rails",
        "pr_number": 53726,
        "pr_file": "railties/lib/rails/generators/test_unit/authentication/templates/test/controllers/sessions_controller_test.rb",
        "discussion_id": "1982842029",
        "commented_code": "@@ -0,0 +1,31 @@\n+require \"test_helper\"\n+\n+class SessionsControllerTest < ActionDispatch::IntegrationTest\n+  test \"new\" do\n+    get new_session_url\n+    assert_response :success\n+  end\n+\n+  test \"create with valid credentials\" do\n+    post session_url, params: { email_address: \"one@example.com\", password: \"password\" }",
        "comment_created_at": "2025-03-07T14:07:27+00:00",
        "comment_author": "dhh",
        "comment_body": "Yes, think we should do the same `setup { @user = User.take }` as we do in the PasswordsControllerTest \ud83d\udc4d",
        "pr_file_module": null
      },
      {
        "comment_id": "1985119491",
        "repo_full_name": "rails/rails",
        "pr_number": 53726,
        "pr_file": "railties/lib/rails/generators/test_unit/authentication/templates/test/controllers/sessions_controller_test.rb",
        "discussion_id": "1982842029",
        "commented_code": "@@ -0,0 +1,31 @@\n+require \"test_helper\"\n+\n+class SessionsControllerTest < ActionDispatch::IntegrationTest\n+  test \"new\" do\n+    get new_session_url\n+    assert_response :success\n+  end\n+\n+  test \"create with valid credentials\" do\n+    post session_url, params: { email_address: \"one@example.com\", password: \"password\" }",
        "comment_created_at": "2025-03-07T14:07:50+00:00",
        "comment_author": "dhh",
        "comment_body": "(And then do as you suggest here, so the tests don't break when you start adding/changing the fixtures).",
        "pr_file_module": null
      }
    ]
  }
]
