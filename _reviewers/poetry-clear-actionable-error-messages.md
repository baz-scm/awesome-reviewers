---
title: Clear actionable error messages
description: Error messages should be user-friendly, readable, and provide actionable
  guidance for resolution. Avoid exposing technical implementation details like raw
  dictionaries, regex patterns, or internal data structures to end users. Instead,
  format errors clearly and include specific steps users can take to resolve the issue.
repository: python-poetry/poetry
label: Error Handling
language: Python
comments_count: 6
repository_stars: 33496
---

Error messages should be user-friendly, readable, and provide actionable guidance for resolution. Avoid exposing technical implementation details like raw dictionaries, regex patterns, or internal data structures to end users. Instead, format errors clearly and include specific steps users can take to resolve the issue.

When validation fails or errors occur, provide context about what went wrong and suggest concrete next steps. For example, instead of showing raw validation output like `{'errors': ['project.name must match pattern ^([a-zA-Z\\d]|[a-zA-Z\\d][\\w.-]*[a-zA-Z\\d])$']}`, format it as:

```python
# Bad - exposes technical details
self.line_error(f"<error>Validation failed: {validation_results}</error>")

# Good - clear and actionable
self.line_error(
    "<error>"
    "Error: poetry.lock is not consistent with pyproject.toml. "
    "Run `poetry lock [--no-update]` to fix it."
    "</error>"
)
```

Consider your audience - error messages should be understandable by developers of all experience levels. When technical details are necessary, provide them in debug/verbose modes while keeping the default error message focused on what the user needs to do to resolve the issue.