---
title: optimize test fixtures
description: Use the `fab!` shorthand syntax for creating test fixtures and reuse
  fabricated objects across tests to improve performance and maintainability. The
  `fab!` method creates objects once per test context and reuses them, reducing database
  overhead compared to creating new objects for each test.
repository: discourse/discourse
label: Testing
language: Ruby
comments_count: 5
repository_stars: 44898
---

Use the `fab!` shorthand syntax for creating test fixtures and reuse fabricated objects across tests to improve performance and maintainability. The `fab!` method creates objects once per test context and reuses them, reducing database overhead compared to creating new objects for each test.

**Preferred approach:**
```ruby
fab!(:theme_1, :theme)
fab!(:theme_2, :theme) 
fab!(:tag_1, :tag)
let(:tags) { [tag_1, tag_2, tag_3] }
```

**Instead of:**
```ruby
fab!(:theme_1) { Fabricate(:theme) }
fab!(:theme_2) { Fabricate(:theme) }
let(:tags) { 3.times.collect { Fabricate(:tag) } }
```

When possible, reuse top-level fabricated objects in nested contexts rather than creating new ones. For example, use `event = Fabricate(:event, post: admin_post)` instead of `post = Fabricate(:post, user: Fabricate(:admin))` when an admin_post fixture already exists at the top level. This approach reduces test setup time, improves readability, and makes test dependencies more explicit.