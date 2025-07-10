---
title: Document non-obvious decisions
description: Always add clear comments explaining non-obvious code decisions such
  as magic numbers, arbitrary values, truncation limits, or special case handling.
  Convert magic numbers to named constants with explanatory comments when appropriate.
  This documentation helps future developers understand the reasoning behind code
  decisions and makes maintenance easier.
repository: Homebrew/brew
label: Documentation
language: Ruby
comments_count: 3
repository_stars: 44168
---

Always add clear comments explaining non-obvious code decisions such as magic numbers, arbitrary values, truncation limits, or special case handling. Convert magic numbers to named constants with explanatory comments when appropriate. This documentation helps future developers understand the reasoning behind code decisions and makes maintenance easier.

For magic numbers in code:
```ruby
# Read enough bytes to detect HTML doctype while limiting file I/O
if File.read(filepath, 100).strip.downcase.start_with?(html_doctype_prefix)
```

For truncation limits:
```ruby
# Maximum length of PR body is 65,536 characters so let's truncate release notes to half of that
body = github_release_data["body"].truncate(32_768)
```

For complex logic:
```ruby
# These formulae must build on Intel macOS because they're required for CLT installation
NEW_INTEL_MACOS_MUST_BUILD_FORMULAE = %w[pkg-config pkgconf].freeze
```

Code without explanatory comments creates a burden for maintainers, forcing them to reverse-engineer the original author's intent. Well-documented decisions reduce the cognitive load for future developers and decrease the likelihood of introducing bugs during modifications.