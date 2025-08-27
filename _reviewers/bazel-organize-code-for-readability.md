---
title: Organize code for readability
description: Structure code to minimize complexity and improve readability through
  logical organization. This includes using early returns to reduce nesting levels
  and ordering operations in a logical sequence.
repository: bazelbuild/bazel
label: Code Style
language: Python
comments_count: 2
repository_stars: 24489
---

Structure code to minimize complexity and improve readability through logical organization. This includes using early returns to reduce nesting levels and ordering operations in a logical sequence.

Use early returns to flatten code structure and avoid deep nesting:

```python
# Prefer this - early return pattern
if argv[1] != "get":
    eprint("Unknown command ...")
    return 1

# Handle main logic here
...

# Instead of nested if-else chains
if argv[1] == "get":
    # Handle main logic here
    ...
else:
    eprint("Unknown command ...")
    return 1
```

Additionally, organize method calls in logical order where setup operations precede execution operations:

```python
# Setup first
self.ScratchFile('BUILD', [...])
self.ScratchFile('main.cc', [...])

# Then execute
exit_code, _, stderr = self.RunBazel([...])
```

This approach reduces cognitive load by keeping indentation shallow and presenting operations in their natural sequence.