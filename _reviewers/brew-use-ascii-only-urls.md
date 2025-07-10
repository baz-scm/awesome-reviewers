---
title: Use ASCII-only URLs
description: URLs in code should exclusively use ASCII characters for maximum security
  and compatibility. This prevents potential security vulnerabilities like homograph
  attacks and ensures consistent behavior across systems.
repository: Homebrew/brew
label: Networking
language: Ruby
comments_count: 3
repository_stars: 44168
---

URLs in code should exclusively use ASCII characters for maximum security and compatibility. This prevents potential security vulnerabilities like homograph attacks and ensures consistent behavior across systems.

For domain names with non-ASCII characters:
- Use Punycode encoding (e.g., `xn--` prefixed domains)

For path and query components:
- Use proper URL encoding for any non-ASCII characters

When validating URLs, include checks to ensure they contain only ASCII characters. Provide clear error messages to guide users toward the proper encoding.

Example:
```ruby
# Incorrect: URLs with non-ASCII characters
url = "https://🫠.sh/foo/bar"
url = "https://ßreｗ.sh/foo/bar"

# Correct: Use ASCII representations
url = "https://xn--sh-9ij.sh/foo/bar"  # Punycode for domain
url = "https://brew.sh/foo%E4%B8%AD%E6%96%87/bar"  # URL encoding for path

# For validation, use a regex to detect non-ASCII characters
ascii_pattern = /[^\p{ASCII}]+/
if url.match?(ascii_pattern)
  puts "Please use the ASCII (Punycode, URL encoded) version of #{url}."
end
```