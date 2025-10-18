---
title: document test configurations
description: When modifying test configurations or tooling settings, provide clear
  explanations of what the changes actually do and why specific options were chosen.
  Test configuration changes can be confusing without proper context.
repository: jj-vcs/jj
label: Testing
language: Toml
comments_count: 2
repository_stars: 21171
---

When modifying test configurations or tooling settings, provide clear explanations of what the changes actually do and why specific options were chosen. Test configuration changes can be confusing without proper context.

For commit messages, explain the current behavior and what's being changed:
```
# Good
nextest: mark tests that last >10s as "SLOW"

Nextest currently marks tests as SLOW if they take more than 5 seconds.
This increases the threshold to 10 seconds to reduce noise.

# Avoid
nextest: mark tests that last >10s as "SLOW"
```

For configuration files, consider adding comments explaining non-obvious settings:
```toml
[tasks."check:test"]
tools."cargo:cargo-nextest" = "{{vars.cargo_nextest_version}}"
# Show slow and retried tests to balance informativeness with readability
env.NEXTEST_STATUS_LEVEL="slow"
```

This prevents confusion about what configuration changes actually accomplish and helps future maintainers understand the reasoning behind specific test tool settings.