---
title: "Verify documentation references"
description: "When writing or updating documentation, ensure all code examples, installation commands, and project references accurately reflect the current codebase."
repository: "vercel/next.js"
label: "Documentation"
language: "Markdown"
comments_count: 4
repository_stars: 133000
---

When writing or updating documentation, ensure all code examples, installation commands, and project references accurately reflect the current codebase. This includes:

1. Double-check that example names in installation commands match the actual project being documented:
```bash
# INCORRECT
npx create-next-app --example hello-world my-etag-test-app

# CORRECT
npx create-next-app --example etag-test etag-test-app
```

2. Verify that all command examples are up-to-date with the latest CLI parameters and syntax.

3. Include clear explanations of the purpose and functionality of examples rather than generic descriptions:
```markdown
# INSUFFICIENT
This is the most minimal starter for your Next.js project.

# BETTER
This example demonstrates the differences in ETag behavior between Next.js 14 and 15 for static pre-rendered pages.
```

4. When copy-pasting documentation templates, carefully review and update all project-specific references to prevent inaccuracies that could confuse users.

Keeping references accurate prevents user frustration and maintains trust in the documentation.