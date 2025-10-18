---
title: documentation formatting consistency
description: Maintain consistent formatting and style patterns across all documentation
  to improve readability and user experience. This includes using proper shell command
  notation, consistent punctuation choices, and aligned configuration examples.
repository: jj-vcs/jj
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 21171
---

Maintain consistent formatting and style patterns across all documentation to improve readability and user experience. This includes using proper shell command notation, consistent punctuation choices, and aligned configuration examples.

For shell commands, use the `$` prefix with explanatory comments:
```
$ jj upload   # "upload" is an alias using "jj util exec"
```

Choose consistent punctuation throughout documentation (prefer commas over em dashes for better readability):
```
time, exactly how Gerrit wants you to work
```

Maintain consistent configuration patterns across different tools and sections:
```toml
[language-server.rust-analyzer.config.rust-analyzer.rustfmt]
extraArgs = ["+nightly"]
```

This approach ensures that documentation maintains a professional, cohesive appearance and reduces cognitive load for readers by establishing predictable formatting patterns.