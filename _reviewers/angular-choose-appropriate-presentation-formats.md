---
title: Choose appropriate presentation formats
description: Select the most effective format for presenting different types of information
  in documentation. Use tables for structured data with multiple attributes, step-by-step
  explanations for processes, and clear section organization to avoid duplication
  or confusion.
repository: angular/angular
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 98611
---

Select the most effective format for presenting different types of information in documentation. Use tables for structured data with multiple attributes, step-by-step explanations for processes, and clear section organization to avoid duplication or confusion.

For structured data like command options, use tables instead of lists:

```markdown
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--read-only` | boolean | `false` | Only register tools that do not make changes |
| `--local-only` | boolean | `false` | Only register tools that do not require internet |
```

For complex processes, provide detailed step-by-step breakdowns:

```markdown
## How SSG works

Here's what happens when SSG renders your application:

1. Angular analyzes your routes at build time
2. Static HTML files are generated for each specified route
3. The initial page loads from pre-rendered HTML
4. Once loaded, navigation works like a standard CSR application
```

Avoid duplicating content between sections (like API reference and guides) unless adding substantial value through examples or different perspectives. Organize sections with clear, non-overlapping headers that accurately reflect their content scope.