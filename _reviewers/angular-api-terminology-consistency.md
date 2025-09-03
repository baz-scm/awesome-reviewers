---
title: API terminology consistency
description: Maintain consistent, precise terminology throughout API documentation
  and interfaces. Avoid ambiguous or misleading terms that could confuse developers
  about the API's behavior, and use professional language that clearly communicates
  the intended functionality.
repository: angular/angular
label: API
language: Markdown
comments_count: 3
repository_stars: 98611
---

Maintain consistent, precise terminology throughout API documentation and interfaces. Avoid ambiguous or misleading terms that could confuse developers about the API's behavior, and use professional language that clearly communicates the intended functionality.

Key practices:
- Use precise technical terms that accurately describe behavior (e.g., avoid "async signals" when signals are always synchronous)
- Maintain consistent capitalization for technical terms (e.g., always use "HTTP" when not part of an identifier)
- Avoid informal or subjective language like "battle-tested" in favor of objective descriptions
- Eliminate first-person pronouns ("we", "us") in API documentation

Example of improved terminology:
```markdown
// Instead of: "Managing async signals with Resources API"
// Use: "Managing async data with Resources API"

// Instead of: "battle-tested libraries like Zod"  
// Use: "popular open-source libraries like Zod"

// Instead of: "You can define an http resource"
// Use: "You can define an HTTP resource"
```

This ensures developers have a clear, unambiguous understanding of API capabilities and constraints, reducing integration errors and improving the overall developer experience.