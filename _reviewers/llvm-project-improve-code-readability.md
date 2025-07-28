---
title: improve code readability
description: 'When code expressions become complex or difficult to understand at first
  glance, refactor them for better readability. This can be achieved through several
  techniques: extracting complex expressions into well-named variables, using named
  regex groups instead of numeric indices, or reformatting conditional logic into
  more concise forms.'
repository: llvm/llvm-project
label: Code Style
language: Python
comments_count: 2
repository_stars: 33702
---

When code expressions become complex or difficult to understand at first glance, refactor them for better readability. This can be achieved through several techniques: extracting complex expressions into well-named variables, using named regex groups instead of numeric indices, or reformatting conditional logic into more concise forms.

For complex expressions, consider extracting intermediate values:
```python
# Instead of:
rewritten_line = (
    self.current_line[: match.start(2)]
    + str(self.frame_no)
    + self.current_line[match.end(2) :]
)

# Use:
frame_no_index = match.start(2)
rewritten_line = (
    self.current_line[:frame_no_index]
    + str(self.frame_no)
    + self.current_line[frame_no_index:]
)
```

For conditional assignments, prefer concise inline forms when they improve clarity:
```python
# Instead of multi-line conditional blocks:
args.std = (
    ["c++11-or-later"]
    if extension in [".cpp", ".hpp", ".mm"]
    else ["c99-or-later"]
)

# Use:
args.std = [
    "c++11-or-later" if extension in [".cpp", ".hpp", ".mm"] else "c99-or-later"
]
```

The goal is to make code self-documenting and reduce cognitive load for future readers.