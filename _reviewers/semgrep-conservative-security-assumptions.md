---
title: Conservative security assumptions
description: 'When implementing security measures, always err on the side of caution
  by making conservative assumptions about potential risks. This principle applies
  across multiple security contexts:'
repository: semgrep/semgrep
label: Security
language: Other
comments_count: 3
repository_stars: 12598
---

When implementing security measures, always err on the side of caution by making conservative assumptions about potential risks. This principle applies across multiple security contexts:

**Taint Analysis**: If there's any execution path where data could become tainted, treat it as tainted. Use may-analysis approaches that assume the worst-case scenario rather than trying to prove safety.

**Capability Restriction**: Limit access rights to the absolute minimum necessary. Don't pass unnecessary capabilities to callbacks or sub-components, even if they're currently unused.

**Resource Protection**: Implement defensive measures like timeouts to prevent resource exhaustion, even in contexts where attacks seem unlikely.

Example from taint analysis:
```python
def process_data(user_input):
    try:
        safe_data = validate(user_input)
        result = process(safe_data)
    except ValidationError:
        result = user_input  # This path taints result
    
    # Treat result as tainted due to exception path
    return sanitize(result)
```

This conservative approach helps prevent security vulnerabilities by assuming potential attack vectors exist rather than trying to prove they don't.