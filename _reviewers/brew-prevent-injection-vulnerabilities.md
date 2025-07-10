---
title: Prevent injection vulnerabilities
description: Always sanitize input data before using it in sensitive operations to
  prevent injection vulnerabilities. This applies to shell commands, file operations,
  and URL handling.
repository: Homebrew/brew
label: Security
language: Ruby
comments_count: 3
repository_stars: 44168
---

Always sanitize input data before using it in sensitive operations to prevent injection vulnerabilities. This applies to shell commands, file operations, and URL handling.

For shell commands:
```ruby
# VULNERABLE: Direct interpolation of variables into command
full_command = `#{HOMEBREW_BREW_FILE} #{brew_command} #{argument}`

# SECURE: Escape each argument properly
require 'shellwords'
full_command = [HOMEBREW_BREW_FILE, brew_command, argument].compact
                                                         .map { |arg| Shellwords.escape(arg) }
```

For file operations:
```ruby
# VULNERABLE: Using IO.read/Kernel.open with non-constant values
content = IO.read(filepath)

# SECURE: Use File.read instead
content = File.read(filepath)
```

For URL operations:
```ruby
# VULNERABLE: Using URI.open with non-constant values
response = URI.open(generated_url).read

# SECURE: Use URI().open instead
response = URI(generated_url).open.read
```

These patterns help prevent several classes of security vulnerabilities, including command injection, arbitrary file access, and server-side request forgery. Always assume input data could be malicious and handle it accordingly.