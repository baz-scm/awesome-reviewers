---
title: markdown formatting consistency
description: Establish and maintain consistent formatting standards for Markdown files
  to improve readability and maintainability. This includes adhering to line length
  limits and consistent styling choices within documents.
repository: mastodon/mastodon
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 48691
---

Establish and maintain consistent formatting standards for Markdown files to improve readability and maintainability. This includes adhering to line length limits and consistent styling choices within documents.

Key guidelines:
- Hard wrap Markdown files at 80 characters for better diff reviews and readability
- Maintain consistency in link formatting styles within each document (either all footnote-style or all inline)
- Match existing formatting patterns in the codebase when making changes

Example of proper line wrapping:
```markdown
These terms of service (the "Terms") cover your access and use of Server 
Operator's ("Administrator" we," or "us") instance, located at %{domain} 
(the "Instance"). These Terms apply solely to your use of the Instance as 
operated by the Administrator.
```

This approach makes documents easier to read in editors, creates cleaner diffs when links change, and ensures a professional, consistent appearance across all documentation.