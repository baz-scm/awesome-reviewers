---
title: Use relative documentation links
description: Always use relative links instead of absolute links in documentation
  files to enable proper broken link detection and ensure compatibility with documentation
  generators like MkDocs.
repository: stanfordnlp/dspy
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 27813
---

Always use relative links instead of absolute links in documentation files to enable proper broken link detection and ensure compatibility with documentation generators like MkDocs.

Absolute links prevent documentation tools from detecting broken links and can cause navigation issues. MkDocs specifically does not support absolute links by default and will generate warnings for unrecognized absolute paths.

**Problematic (absolute links):**
```markdown
- [Building AI Agents with DSPy](/tutorials/customer_service_agent/)
- [Set Up Observability](../tutorials/observability/#tracing)
```

**Correct (relative links):**
```markdown
- [Building AI Agents with DSPy](../customer_service_agent/index.ipynb)
- [Set Up Observability](../tutorials/observability/index.md#tracing)
```

When linking to sections within other pages, include the full file path with `index.md` to help MkDocs understand the relative link structure. This prevents warnings like "contains an unrecognized relative link" and ensures proper link resolution in the generated documentation.