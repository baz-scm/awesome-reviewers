---
title: Document configuration defaults clearly
description: When documenting configuration options, always specify exact file paths,
  explicit default values, and clarify potentially confusing settings to prevent user
  confusion. This includes documenting where settings are persisted, what happens
  when optional properties are omitted, and explaining any non-obvious behavior like
  token budget comparisons.
repository: google-gemini/gemini-cli
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 65062
---

When documenting configuration options, always specify exact file paths, explicit default values, and clarify potentially confusing settings to prevent user confusion. This includes documenting where settings are persisted, what happens when optional properties are omitted, and explaining any non-obvious behavior like token budget comparisons.

For example, instead of just mentioning "settings are saved," specify the exact location:
```json
// Settings are saved to ~/.gemini/settings.json
"vim": true
```

When documenting optional configuration properties, explicitly state the default behavior:
```json
// authProviderType is optional - omitting it defaults to "dynamic_discovery"
"authProviderType": "dynamic_discovery"  // default
```

For complex configurations that might cause confusion, add clarifying comments:
```json
// tokenBudget is compared against character length as an approximation
"summarizeToolOutput": {
  "run_shell_command": {
    "tokenBudget": 100  // approximate token count, compared to character length
  }
}
```