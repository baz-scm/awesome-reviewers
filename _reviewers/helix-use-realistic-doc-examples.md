---
title: Use realistic doc examples
description: Documentation should include concrete, realistic examples that demonstrate
  practical usage rather than abstract concepts. This helps readers better understand
  the functionality and improves documentation accessibility for all skill levels.
repository: helix-editor/helix
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 39026
---

Documentation should include concrete, realistic examples that demonstrate practical usage rather than abstract concepts. This helps readers better understand the functionality and improves documentation accessibility for all skill levels.

Examples should:
1. Demonstrate real-world use cases
2. Include full context when needed
3. Explain technical terms when used
4. Show practical applications

Good example:
```
# Explaining a git blame command
:echo %sh{git blame -L %{cursor_line},+1 %{buffer_name}}

# Explaining variables
Set a format string for `format` to customize the blame message. 
Variables are text placeholders wrapped in curly braces (`{variable}`).
```

Instead of just describing features abstractly, this approach shows actual usage patterns that readers can relate to and adapt for their needs. When technical terms are necessary, include brief explanations to make the documentation accessible to a wider audience.