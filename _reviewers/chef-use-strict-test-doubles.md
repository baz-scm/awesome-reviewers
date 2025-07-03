---
title: Use strict test doubles
description: Always use strict test doubles (instance_double, class_double) instead
  of basic doubles or OpenStruct in tests. Strict doubles provide compile-time checks
  that prevent tests from passing when the mocked interface changes, improving test
  maintainability and catching integration issues early.
repository: chef/chef
label: Testing
language: Ruby
comments_count: 4
repository_stars: 7860
---

Always use strict test doubles (instance_double, class_double) instead of basic doubles or OpenStruct in tests. Strict doubles provide compile-time checks that prevent tests from passing when the mocked interface changes, improving test maintainability and catching integration issues early.

Example - Instead of:
```ruby
auth_stub = double("vault auth", aws_iam: nil)
dummy = OpenStruct.new(stdout: output, exitstatus: 0)
```

Use:
```ruby
auth_stub = instance_double("VaultAuth", aws_iam: nil)
shell_out = instance_double(Mixlib::ShellOut,
  stdout: output,
  exitstatus: 0,
  error?: false
)
```

This approach:
- Ensures mocks accurately reflect the real interfaces
- Catches interface changes during test execution
- Makes dependencies explicit in test code
- Prevents tests from silently passing with invalid assumptions
