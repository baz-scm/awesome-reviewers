---
title: Simplify complex logic
description: Break down complex code structures into simpler, more readable forms.
  Long indented blocks, verbose conditionals, and repetitive patterns should be simplified
  to improve code clarity and maintainability.
repository: semgrep/semgrep
label: Code Style
language: Python
comments_count: 4
repository_stars: 12598
---

Break down complex code structures into simpler, more readable forms. Long indented blocks, verbose conditionals, and repetitive patterns should be simplified to improve code clarity and maintainability.

Key practices:
- Extract long indented blocks into separate functions to improve readability
- Replace verbose loops with concise built-in operations when possible
- Reorder conditional logic to avoid confusing double negatives
- Use simple variable assignment instead of complex conditional expressions

Examples:

Instead of a verbose loop:
```python
for value in validation_state_metadata.values():
    if value == "block":
        return True
return False
```

Use a concise expression:
```python
return "block" in validation_state_metadata.values()
```

Instead of confusing conditional order:
```python
*(
    (self.start.offset, self.end.offset)
    if not (self.extra.get("sca_info") and not self.extra["sca_info"].reachable)
    else (self.start.line, self.end.line)
),
```

Reorder for clarity:
```python
*(
    (self.start.line, self.end.line)
    if (self.extra.get("sca_info") and not self.extra["sca_info"].reachable)
    else (self.start.offset, self.end.offset)
),
```

This approach reduces cognitive load and makes code easier to understand and maintain.