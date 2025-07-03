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
