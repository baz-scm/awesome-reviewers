---
title: Prioritize naming clarity
description: Choose names that are immediately self-explanatory and unambiguous, even
  if they are more verbose. Names should convey their full meaning and context without
  requiring additional documentation or guesswork.
repository: BerriAI/litellm
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 28310
---

Choose names that are immediately self-explanatory and unambiguous, even if they are more verbose. Names should convey their full meaning and context without requiring additional documentation or guesswork.

When naming variables, configuration settings, or API patterns, prioritize precision over brevity. A longer, descriptive name is preferable to a shorter, ambiguous one.

Examples:
- Prefer `maximum_spend_logs_retention_period` over `maximum_retention_period` to clearly specify what type of retention period is being configured
- Use explicit path structures like `huggingface/<provider>/<hf_org_or_user>/<hf_model>` to make hierarchical relationships and namespacing clear

The goal is that any developer reading the code should immediately understand what a name refers to without needing to consult documentation or make assumptions about its scope or purpose.