---
title: Correct GitHub Actions annotations
description: When using GitHub Actions workflow commands for annotations, always include
  double colons in the syntax (::command::). Proper formatting ensures warnings and
  errors are correctly displayed in the GitHub Actions UI and processed by workflow
  runners.
repository: Homebrew/brew
label: CI/CD
language: Ruby
comments_count: 4
repository_stars: 44168
---

When using GitHub Actions workflow commands for annotations, always include double colons in the syntax (::command::). Proper formatting ensures warnings and errors are correctly displayed in the GitHub Actions UI and processed by workflow runners.

Example:
```ruby
# Correct
puts "::warning::#{message_full}" if ENV["GITHUB_ACTIONS"]
puts "::error::#{message_full}" if ENV["GITHUB_ACTIONS"]

# Incorrect
puts "::warning #{message_full}" if ENV["GITHUB_ACTIONS"]
puts "::error #{message_full}" if ENV["GITHUB_ACTIONS"]
```

Missing the second set of colons will prevent GitHub Actions from properly parsing these annotations, resulting in warnings and errors not being prominently displayed in the workflow run interface. This makes CI/CD issues harder to identify and debug.