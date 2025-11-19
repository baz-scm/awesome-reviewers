---
title: User-centric documentation practices
description: Documentation should prioritize user needs and experience over technical
  convenience. This means using appropriate link types (guides over API docs for user-facing
  content), organizing content to avoid overwhelming newcomers, providing necessary
  context, and ensuring links work correctly with tooling.
repository: nrwl/nx
label: Documentation
language: Markdown
comments_count: 7
repository_stars: 27518
---

Documentation should prioritize user needs and experience over technical convenience. This means using appropriate link types (guides over API docs for user-facing content), organizing content to avoid overwhelming newcomers, providing necessary context, and ensuring links work correctly with tooling.

Key practices:
- Link to comprehensive guides rather than API documentation for user-facing scenarios: `/docs/technologies/testingtools/vitest/guides/migrating-from-nx-vite` instead of API docs
- Structure introductory content to be approachable - avoid leading with advanced technical concepts that might discourage users
- Provide context for UI elements and processes that users might not be familiar with
- Organize related content as subsections rather than separate sections when it improves flow
- Use link formats that work with link checkers (avoid "docs" prefixes that cause validation issues)
- Keep content focused and avoid overwhelming lists in introductory sections

Example of user-centric approach:
```markdown
<!-- Instead of leading with technical details -->
# Build Your Own Nx Plugin: Integrating Biome in 20 Minutes

<!-- Lead with user benefits -->
# Using Biome with Nx: Fast Linting and Formatting
Learn how to integrate Biome for faster linting. You don't need a plugin to get started, but creating one will make your workflow smoother.
```

This approach ensures documentation serves users effectively rather than just being technically accurate.