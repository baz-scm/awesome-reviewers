---
title: telemetry documentation consistency
description: Maintain consistent formatting and style when documenting telemetry and
  observability systems. This includes using parallel structure in lists, consistent
  terminology, and clear explanations of what data is collected and why.
repository: cloudflare/workers-sdk
label: Observability
language: Markdown
comments_count: 2
repository_stars: 3379
---

Maintain consistent formatting and style when documenting telemetry and observability systems. This includes using parallel structure in lists, consistent terminology, and clear explanations of what data is collected and why.

When documenting telemetry collection, ensure:
- List items follow parallel grammatical structure
- Consistent phrasing across similar concepts (e.g., "Package manager" vs "Package manager being used")
- Clear, professional language that explains the purpose and scope of data collection
- Proper punctuation and formatting throughout

Example of inconsistent vs consistent formatting:
```markdown
// Inconsistent
- What command is used as the entrypoint?
- Package manager being used (e.g. npm, yarn)  
- Number of first time downloads

// Consistent  
- Command used as entrypoint
- Package manager (e.g. npm, yarn)
- Whether instance is a first-time download
```

This ensures that observability documentation is professional, clear, and maintains user trust by transparently communicating monitoring practices.