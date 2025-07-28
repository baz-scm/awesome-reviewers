---
title: validate configuration values
description: Always validate configuration values and provide clear, actionable error
  messages when validation fails. Handle invalid values gracefully by either ignoring
  them or providing sensible defaults, and validate that configuration options are
  used in the correct context.
repository: prettier/prettier
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 50772
---

Always validate configuration values and provide clear, actionable error messages when validation fails. Handle invalid values gracefully by either ignoring them or providing sensible defaults, and validate that configuration options are used in the correct context.

Key practices:
- Check for invalid values and ignore them rather than crashing: `if (tabWidth === 0) { /* ignore invalid value */ }`
- Validate configuration dependencies with clear error messages: `"--cache-strategy cannot be used without --cache"`
- Ensure configuration options are available in the expected context before using them
- Provide helpful suggestions when validation fails, such as suggesting similar valid options
- Handle edge cases like empty arrays or missing context gracefully: `if (ignoreFilePaths.length === 0 && !withNodeModules) { ignoreFilePaths = [undefined]; }`

This prevents runtime crashes, improves user experience, and makes configuration errors easier to debug and fix.