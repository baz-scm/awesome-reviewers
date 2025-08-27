---
title: Structure documentation logically
description: Organize documentation sections and content to match user mental models
  and workflows, not internal technical implementation details. Use descriptive, specific
  section names instead of generic ones like "Other changes" or overly technical terms.
  Present information in the order users will encounter or need it, prioritizing common
  use cases before advanced...
repository: astral-sh/ty
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 11919
---

Organize documentation sections and content to match user mental models and workflows, not internal technical implementation details. Use descriptive, specific section names instead of generic ones like "Other changes" or overly technical terms. Present information in the order users will encounter or need it, prioritizing common use cases before advanced configuration options.

For example, when documenting configuration options, lead with default behavior that most users will experience, then explain override mechanisms:

```markdown
# Good: User-centric organization
## Python environment

By default, ty searches for a `.venv` folder in the project root. If the `VIRTUAL_ENV` environment variable is set, ty will use that path instead.

The Python environment can also be explicitly specified using the `--python` flag...

# Better section naming
## Typing semantics and features
(instead of "Other changes")

## Logging options  
(instead of "Initialization options" when content is logging-specific)
```

Consider future extensibility when naming sections - avoid overly specific names that may need renaming as features expand. Structure content to minimize cognitive load by following the user's natural workflow and decision-making process.