---
title: Provide specific examples
description: Documentation should include concrete, actionable examples and use clear,
  unambiguous terminology to eliminate confusion for developers. Avoid vague instructions
  that leave developers guessing about implementation details.
repository: cloudflare/workers-sdk
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 3379
---

Documentation should include concrete, actionable examples and use clear, unambiguous terminology to eliminate confusion for developers. Avoid vague instructions that leave developers guessing about implementation details.

When documenting commands or procedures, provide specific examples rather than generic descriptions. For instance, instead of writing "run uninstall", specify the exact command: `npm uninstall @cloudflare/workers-types`.

Choose terminology that is precise and contextually clear. Consider how terms might be interpreted differently in various contexts - for example, "Worker environments" could be confusing when discussing both Cloudflare Workers and Vite environments, so "Cloudflare environments" would be more specific and less ambiguous.

This approach helps developers understand exactly what actions to take and reduces the cognitive load of interpreting documentation.