---
title: Prevent duplicate keys
description: Always ensure configuration files, especially JSON files, have unique
  keys. Duplicate keys can cause unpredictable behavior as the last occurrence of
  a key will overwrite previous values, potentially leading to runtime errors or inconsistent
  application behavior.
repository: RooCodeInc/Roo-Code
label: Configurations
language: Json
comments_count: 5
repository_stars: 17288
---

Always ensure configuration files, especially JSON files, have unique keys. Duplicate keys can cause unpredictable behavior as the last occurrence of a key will overwrite previous values, potentially leading to runtime errors or inconsistent application behavior.

When adding new configuration:
- Check for existing keys with the same name
- Use a linter or validator to detect duplicate keys
- Merge related properties into a single, unified object structure

Example of problematic code:
```json
{
  "codeIndex": {
    "setting1": "value1"
  },
  // Other settings...
  "codeIndex": {
    "setting2": "value2"
  }
}
```

Correct approach:
```json
{
  "codeIndex": {
    "setting1": "value1",
    "setting2": "value2"
  }
  // Other settings...
}
```

This is especially critical in localization files and application configuration where duplicate keys can lead to missing translations or incorrect settings being applied.