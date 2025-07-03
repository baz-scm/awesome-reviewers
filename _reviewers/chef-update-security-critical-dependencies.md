---
title: Update security-critical dependencies
description: Regularly audit and update third-party libraries and dependencies to
  address known security vulnerabilities. Pay special attention to components that
  handle sensitive operations such as file system access, encryption, or network communication.
  Implement a systematic process to monitor CVEs and security bulletins relevant to
  your dependencies, and document...
repository: chef/chef
label: Security
language: Markdown
comments_count: 1
repository_stars: 7860
---

Regularly audit and update third-party libraries and dependencies to address known security vulnerabilities. Pay special attention to components that handle sensitive operations such as file system access, encryption, or network communication. Implement a systematic process to monitor CVEs and security bulletins relevant to your dependencies, and document all security-related updates in release notes with specific vulnerability references.

Example:
```ruby
# In your dependency management file (e.g., Gemfile, package.json, requirements.txt)

# GOOD: Specify minimum secure versions with comments explaining security implications
gem 'libarchive', '>= 3.5.2'  # Addresses symbolic link handling vulnerabilities
gem 'openssl', '>= 1.1.1l'    # Resolves CVE-2021-3711 and CVE-2021-3712

# BETTER: Include automated security scanning in your CI pipeline
# Example GitHub Actions workflow snippet:
- name: Security scan dependencies
  uses: some-security-scanner-action@v1
  with:
    scan-type: 'dependency'
    fail-on: 'high'
```

When updating dependencies for security reasons, always include clear documentation in your release notes that specifies:
1. Which dependency was updated
2. The version change (from/to)
3. What security vulnerability was addressed
4. Any potential impact on existing functionality
