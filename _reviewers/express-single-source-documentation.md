---
title: Single source documentation
description: Maintain documentation with a single source of truth to prevent inconsistencies
  and reduce maintenance burden. When information exists elsewhere, link to it rather
  than duplicating content. This applies to code of conduct references, governance
  documents, and API documentation.
repository: expressjs/express
label: Documentation
language: Markdown
comments_count: 8
repository_stars: 67300
---

Maintain documentation with a single source of truth to prevent inconsistencies and reduce maintenance burden. When information exists elsewhere, link to it rather than duplicating content. This applies to code of conduct references, governance documents, and API documentation.

For example:
```markdown
// Good - Links to the source
The code of conduct is located in [CODE_OF_CONDUCT.md](https://github.com/expressjs/.github/blob/HEAD/CODE_OF_CONDUCT.md)

// Bad - Duplicates content that might get out of sync
# Code of Conduct
Our project is committed to providing a welcoming community...
```

When writing documentation:
1. Use consistent formatting and third-person voice throughout
2. Convert bullet points to paragraphs for complex explanations
3. Organize content logically with clear section headers
4. Provide relative links to related documentation
5. Consider where documentation should live to minimize repository clutter

By following these practices, documentation stays current, accurate, and easier to maintain as the project evolves. When documentation must exist in multiple locations, establish clear processes for synchronization.