---
title: Official product naming
description: When referencing external products, libraries, or services in documentation
  and code, always use their official names exactly as specified by the vendor, and
  treat them as proper nouns without articles.
repository: prisma/prisma
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 42967
---

When referencing external products, libraries, or services in documentation and code, always use their official names exactly as specified by the vendor, and treat them as proper nouns without articles.

Key principles:
- Use official product names without modification (e.g., "Cloudflare D1" not "Cloudflare's Serverless Driver D1")
- Treat product names as proper nouns - don't prefix with articles like "the" (e.g., "Prisma Client" not "the Prisma Client")
- Maintain consistency across all documentation and comments

Example from documentation:
```markdown
// Incorrect
Install the Prisma Client, the Prisma adapter for Cloudflare's Serverless Driver D1

// Correct  
Install Prisma Client, Prisma adapter for Cloudflare D1
```

This ensures accuracy, professionalism, and consistency when referencing third-party technologies, while avoiding confusion about official product capabilities or features.