---
title: Provide contextual explanations
description: Documentation should explain the reasoning, context, and practical implications
  behind code examples, not just show syntax or commands. Include explanations of
  why developers would use specific approaches, how different options work together,
  and what to expect from running commands.
repository: serverless/serverless
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 46810
---

Documentation should explain the reasoning, context, and practical implications behind code examples, not just show syntax or commands. Include explanations of why developers would use specific approaches, how different options work together, and what to expect from running commands.

For example, instead of just showing configuration syntax:
```yaml
custom:
  esbuild:
    sourcemap: true
```

Provide context about when and why:
```yaml
# Enable source maps for better error debugging in transpiled code
custom:
  esbuild:
    sourcemap: true
```

When documenting commands, explain their purpose and expected outcomes rather than using vague phrases like "follow the prompts." Replace complex, deployment-specific examples with simpler, more universally applicable ones that developers can easily understand and adapt to their needs.