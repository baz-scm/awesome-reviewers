---
title: Include concrete examples
description: Technical documentation should always include concrete, working examples
  that demonstrate the described concepts in action. Examples clarify abstract ideas,
  illustrate correct usage patterns, and provide templates users can adapt to their
  needs.
repository: continuedev/continue
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 27819
---

Technical documentation should always include concrete, working examples that demonstrate the described concepts in action. Examples clarify abstract ideas, illustrate correct usage patterns, and provide templates users can adapt to their needs.

When writing documentation:
- Include at least one practical example for each feature, API, or configuration option
- Show both the syntax and the expected output or behavior when applicable
- Use realistic scenarios that reflect common use cases
- For complex features, provide multiple examples showing different options or configurations

For example, when documenting a prompt template feature:

```yaml
# Example prompt template configuration
promptTemplates:
  autocomplete:
    template: |
      Complete the following code in {{language}}:
      File: {{{filename}}}
      
      {{{prefix}}}
      
      # Continue the code here, completing the current statement or function
```

Examples make documentation more effective by transforming abstract concepts into concrete implementations that users can understand and adapt to their specific needs.