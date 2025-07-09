---
title: Document configuration alternatives
description: When documenting commands or tools that can be executed in different
  ways based on configuration settings (like global vs. local installation), always
  explicitly describe all alternatives with clear, consistent labeling. Include examples
  for each configuration option to ensure users can follow instructions regardless
  of their environment setup.
repository: vercel/turborepo
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 28115
---

When documenting commands or tools that can be executed in different ways based on configuration settings (like global vs. local installation), always explicitly describe all alternatives with clear, consistent labeling. Include examples for each configuration option to ensure users can follow instructions regardless of their environment setup.

For example:
```
# With global installation
turbo dev

# Without global installation, use your package manager
npx turbo dev
yarn exec turbo dev
pnpm exec turbo dev
```

This approach makes documentation more inclusive and prevents confusion when users have different environment configurations. It's especially important for tools that offer multiple execution paths depending on how they're installed or configured.