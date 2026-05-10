---
title: Doc Intro And Links
description: 'For roadmap/technical documentation pages, follow these rules:


  - **Use correct Markdown structure**: prefer headings (e.g., `## Section`) over
  HTML line breaks like `<br/>`.'
repository: kamranahmedse/developer-roadmap
label: Documentation
language: Markdown
comments_count: 8
repository_stars: 354523
---

For roadmap/technical documentation pages, follow these rules:

- **Use correct Markdown structure**: prefer headings (e.g., `## Section`) over HTML line breaks like `<br/>`.
- **Keep pages intro-only**: when the page is meant to be a brief overview, **avoid adding code examples**; instead, explain the concept briefly and **redirect to external resources**.
- **Follow strict “resources” link conventions**:
  - Use the correct **link type tag** (e.g., `@article`, `@official`, `@roadmap`) for the resource.
  - Prefer **official** sources first; include a **small number of supporting article links** (e.g., ~2), rather than many.
  - Ensure URLs are in the correct form for your system:
    - If the environment requires copy/paste compatibility, keep **full URLs**.
    - If other pages use paths, keep the expected path structure consistently.

Example (intro without code + clean heading + resources):

```md
## Example (concept only)

This page provides a brief introduction to the concept and what it’s used for.
For deeper details and usage, see the resources below.

Learn more from the following resources:

- [@official@Concept Overview](https://example.com/official)
- [@article@Concept Deep Dive](https://example.com/deep-dive)
- [@article@Best Practices](https://example.com/best-practices)
```

Applying this consistently will improve readability, reduce duplicated content, and prevent broken/incorrect resource links.