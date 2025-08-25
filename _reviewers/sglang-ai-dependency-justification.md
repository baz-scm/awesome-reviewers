---
title: AI dependency justification
description: When modifying AI library dependencies, always provide clear justification
  for version choices, especially when using non-standard sources like git commits
  or release candidates. This is critical for AI projects where library compatibility
  and stability directly impact model performance and inference reliability.
repository: sgl-project/sglang
label: AI
language: Toml
comments_count: 2
repository_stars: 17245
---

When modifying AI library dependencies, always provide clear justification for version choices, especially when using non-standard sources like git commits or release candidates. This is critical for AI projects where library compatibility and stability directly impact model performance and inference reliability.

For standard version updates, explain the motivation (bug fixes, new features, compatibility requirements). For non-standard sources like git commits, document:
- The specific issue being resolved
- Why the official release is insufficient
- Plans for migrating back to official releases

Example of good justification:
```python
# Using git commit due to bug in official v4.49.0 that affects vision models
"transformers @ git+https://github.com/huggingface/transformers.git@84f0186",
# TODO: Migrate back to official release when v4.49.1+ is available
```

This practice prevents confusion during code reviews, helps with dependency auditing, and ensures the team understands the rationale behind critical AI library choices that could affect model behavior or performance.