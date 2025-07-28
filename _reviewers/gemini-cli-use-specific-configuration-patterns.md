---
title: Use specific configuration patterns
description: When defining exclusion patterns, file filters, or other configuration
  rules, use specific, targeted patterns rather than broad glob patterns. Overly broad
  patterns can lead to unintended exclusions and hard-to-debug issues in the future
  when legitimate files need to be included.
repository: google-gemini/gemini-cli
label: Configurations
language: Json
comments_count: 5
repository_stars: 65062
---

When defining exclusion patterns, file filters, or other configuration rules, use specific, targeted patterns rather than broad glob patterns. Overly broad patterns can lead to unintended exclusions and hard-to-debug issues in the future when legitimate files need to be included.

For example, instead of using a broad pattern like `!dist/**/*.tgz` that excludes all .tgz files from any subdirectory, use a specific pattern like `!dist/google-gemini-cli-core-*.tgz` that targets only the intended files. This approach:

- Makes the configuration intent explicit and self-documenting
- Prevents accidental exclusion of legitimate files
- Reduces maintenance risk and potential regressions
- Avoids hard-to-debug issues when requirements change

```json
{
  "files": [
    "dist",
    "!dist/google-gemini-cli-core-*.tgz"  // Specific pattern
  ]
}
```

This principle applies to all configuration contexts including package.json files arrays, .gitignore patterns, build tool configurations, and other rule-based settings.