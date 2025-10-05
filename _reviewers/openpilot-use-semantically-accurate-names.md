---
title: Use semantically accurate names
description: Variable, method, and class names should accurately reflect their actual
  behavior and purpose. Misleading or vague names create confusion and make code harder
  to understand and maintain.
repository: commaai/openpilot
label: Naming Conventions
language: Python
comments_count: 9
repository_stars: 58214
---

Variable, method, and class names should accurately reflect their actual behavior and purpose. Misleading or vague names create confusion and make code harder to understand and maintain.

Key principles:
- Names should describe what the code element actually does, not what it was originally intended to do
- Avoid generic names when specific ones are more appropriate
- Choose names that eliminate ambiguity about the element's role or state

Examples of improvements:
```python
# Bad: misleading name
params_reader.put_nonblocking("LiveParameters", msg_dat)  # writes but called "reader"

# Good: accurate name
params_writer.put_nonblocking("LiveParameters", msg_dat)

# Bad: vague name
def switchEsimProfile(iccid: str):

# Good: clear action
def setEsimProfile(iccid: str):

# Bad: ambiguous state
"ENABLED": 1  # could mean active or just available

# Good: specific meaning
"LKAS_AVAILABLE": 1

# Bad: generic name
def daemon_alive(cam):

# Good: descriptive purpose
def camera_thread(cam):
```

When reviewing names, ask: "Does this name accurately describe what this code element actually does or represents?" If there's any ambiguity or mismatch between the name and behavior, suggest a more precise alternative.