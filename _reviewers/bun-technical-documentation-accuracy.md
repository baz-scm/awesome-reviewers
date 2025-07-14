---
title: Technical documentation accuracy
description: 'Documentation must precisely reflect the current state of the codebase
  to prevent confusion and ensure developers can rely on it. Ensure that:


  1. References to packages, tools, or features that have been removed or renamed
  are updated or deleted from documentation'
repository: oven-sh/bun
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 79093
---

Documentation must precisely reflect the current state of the codebase to prevent confusion and ensure developers can rely on it. Ensure that:

1. References to packages, tools, or features that have been removed or renamed are updated or deleted from documentation
2. Technical specifications (architectures, versions, etc.) accurately match the actual components they describe
3. Configuration options and parameters are described using correct terminology that reflects their actual type and function

Example of correct documentation:
```markdown
You can run the test suite either using `bun test <path>` or by using the wrapper script `bun node:test <path>`. The `bun node:test` command runs every test file in a separate instance of bun.exe, to prevent a crash in the test runner from stopping the entire suite.
```

Rather than referencing deleted packages or using imprecise terminology, this accurately describes the current testing capabilities and their behavior.