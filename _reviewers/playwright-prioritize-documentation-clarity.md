---
title: Prioritize documentation clarity
description: Documentation should prioritize clarity and actionable guidance over
  comprehensive coverage. Organize content logically by placing the most relevant
  information first, provide clear recommendations on preferred approaches, and avoid
  unnecessary complexity or redundant details that don't add value.
repository: microsoft/playwright
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 76113
---

Documentation should prioritize clarity and actionable guidance over comprehensive coverage. Organize content logically by placing the most relevant information first, provide clear recommendations on preferred approaches, and avoid unnecessary complexity or redundant details that don't add value.

Key principles:
- Structure content to guide users toward the best practices (e.g., "you should use config option instead" rather than just explaining alternatives)
- Remove redundant information that can diverge from authoritative sources
- Focus on essential information and avoid "unnecessary details for the default mode"
- Provide clear, actionable guidance that helps users "immediately understand what to do"

Example of good practice:
```markdown
:::note
The `context.tracing` API records different information than the automatic tracing enabled through [Playwright Test configuration](https://playwright.dev/docs/api/class-testoptions#test-options-trace). For most use cases, you should use the configuration option instead as it captures both browser operations and test assertions.
:::
```

This approach ensures documentation serves as an effective guide rather than just a comprehensive reference, helping users make informed decisions quickly.