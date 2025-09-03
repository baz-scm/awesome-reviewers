---
title: Consistent formatting standards
description: Maintain consistent formatting and syntax across all documentation and
  code examples to improve readability and functionality. Follow established style
  guides and ensure uniformity in presentation.
repository: langflow-ai/langflow
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 111046
---

Maintain consistent formatting and syntax across all documentation and code examples to improve readability and functionality. Follow established style guides and ensure uniformity in presentation.

For documentation formatting, use consistent patterns for optional steps and procedures. For example, format optional steps as "Optional:" rather than "(Optional)" following Google's style guide:

```markdown
3. Optional: Install pre-commit hooks to help keep your changes clean and well-formatted.
```

For code examples, standardize quote usage throughout all examples. Use double quotes for headers and variables that need expansion:

```bash
curl -X POST \
  "http://localhost:7860/api/v1/webhook/YOUR_FLOW_ID" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $LANGFLOW_API_KEY" \
```

This ensures both visual consistency and functional correctness, as single quotes prevent variable expansion while double quotes allow it.