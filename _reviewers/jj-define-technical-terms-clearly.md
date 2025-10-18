---
title: Define technical terms clearly
description: Always define technical terms and concepts explicitly in documentation
  rather than assuming reader knowledge. Avoid ambiguous phrasing that could be interpreted
  multiple ways.
repository: jj-vcs/jj
label: Documentation
language: Markdown
comments_count: 10
repository_stars: 21171
---

Always define technical terms and concepts explicitly in documentation rather than assuming reader knowledge. Avoid ambiguous phrasing that could be interpreted multiple ways.

When introducing technical terms:
- Provide clear, concise definitions inline rather than relying solely on external links
- Use precise language that eliminates ambiguity
- Be explicit about technical concepts even if they seem obvious

Examples of good practice:
```markdown
# Good: Clear definition
* `.trailers() -> List<Trailer>`: The trailers at the end of the commit 
  description that are formatted as `<key>: <value>`.

# Bad: Ambiguous phrasing  
* `.trailers() -> List<Trailer>`: The trailers at the end of the commit
  description, formatted as `<key>: <value>`.
```

```markdown
# Good: Precise terminology
* `.synced() -> Boolean`: For a local bookmark, true if synced with all tracked remotes.

# Bad: Imprecise terminology
* `.synced() -> Boolean`: For a local bookmark, true if synced with all remotes.
```

This prevents confusion, reduces the need for readers to maintain external references, and ensures documentation is self-sufficient. Pay special attention to terms that may have different meanings in different contexts or tools.