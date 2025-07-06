---
title: Document configuration clearly
description: 'When adding or modifying configuration parameters, especially in JSON
  settings files, ensure they are clearly documented with comments that explain:

  1. The purpose of the parameter'
repository: zed-industries/zed
label: Code Style
language: Json
comments_count: 2
repository_stars: 62119
---

When adding or modifying configuration parameters, especially in JSON settings files, ensure they are clearly documented with comments that explain:
1. The purpose of the parameter
2. The unit of measurement for numeric values
3. Whether the value is a default, minimum, or maximum
4. Any constraints or considerations

Use descriptive names rather than cryptic ones, and consider uncommenting default values to make them explicit to users. This improves maintainability and helps prevent confusion.

Example:
```json
"inline": {
  // Whether to show diagnostics inline or not
  "enabled": false,
  // The delay in milliseconds to show inline diagnostics after the
  // last buffer update.
  "delay_ms": 0,
  // The amount of padding between the end of the source line and the start
  // of the inline diagnostic in units of columns.
  "padding": 6
}
```

For context names, prefer clear, concise descriptors that convey meaning rather than listing all conditions explicitly:

```json
// Instead of:
"context": "Editor && showing_multiple_signature_help && !showing_completions"

// Prefer:
"context": "Editor && can_scroll_signature_help"
```