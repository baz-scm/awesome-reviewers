---
title: document test tool options
description: When documenting test tools, migration utilities, or testing frameworks,
  provide comprehensive explanations of different modes or options available, including
  their trade-offs and appropriate use cases. This helps developers make informed
  decisions about which approach best fits their testing needs.
repository: prometheus/prometheus
label: Testing
language: Markdown
comments_count: 3
repository_stars: 59616
---

When documenting test tools, migration utilities, or testing frameworks, provide comprehensive explanations of different modes or options available, including their trade-offs and appropriate use cases. This helps developers make informed decisions about which approach best fits their testing needs.

Key elements to include:
- Clear description of what each option does
- Trade-offs and implications of each choice
- Guidance on when to use each option
- Examples showing the differences in behavior

For example, when documenting a test migration tool:

```
The `--mode` flag controls how expectations are migrated:
- `strict`: Strictly migrates all expectations to the new syntax.
  This is probably more verbose than intended because the old syntax
  implied many constraints that are often not needed.
- `basic`: Like `strict` but never creates `no_info` and `no_warn`
  expectations. This can be a good starting point to manually add 
  `no_info` and `no_warn` expectations and/or remove `info` and 
  `warn` expectations as needed.
- `tolerant`: Only creates `expect fail` and `expect ordered` where
  appropriate. All desired expectations about presence or absence 
  of `info` and `warn` have to be added manually.
  
All three modes create valid passing tests from previously passing tests.
`basic` and `tolerant` just test fewer expectations than the previous tests.
```

This approach prevents confusion and helps teams choose the right testing strategy for their specific context.