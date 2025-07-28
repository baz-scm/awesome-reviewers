---
title: Classify configuration properties appropriately
description: Ensure configuration properties and settings are properly categorized
  based on their intended use, visibility, and user interaction requirements. Built-in
  system properties should be classified as hidden, editable, or user-visible depending
  on whether end users should interact with them directly.
repository: logseq/logseq
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 37695
---

Ensure configuration properties and settings are properly categorized based on their intended use, visibility, and user interaction requirements. Built-in system properties should be classified as hidden, editable, or user-visible depending on whether end users should interact with them directly.

For built-in properties that control system behavior:
- Use `hidden-built-in-properties` for internal system properties that users should never see or modify
- Use `editable-built-in-properties` for system properties that users can modify but shouldn't clutter UI elements like query builders
- Avoid exposing internal configuration properties in user-facing interfaces unless explicitly needed

For user-facing configuration options:
- Provide multiple installation/setup methods to accommodate different user preferences and environments
- Document all available configuration approaches rather than removing options
- Consider cross-platform compatibility when designing configuration workflows

Example from the codebase:
```javascript
// Good: Properly categorized table properties
const editableBuiltInProperties = [
  'logseq.table.version',
  'logseq.table.hover', 
  'logseq.table.stripes'
];

// Avoid: Exposing internal properties in user UI
// These shouldn't appear in query builder dropdowns
```

This ensures users can configure what they need without being overwhelmed by internal system properties, while maintaining flexibility for different development environments and user preferences.