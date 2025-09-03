---
title: Configuration documentation completeness
description: Configuration documentation should include all necessary constraints
  and limitations while avoiding redundant information that's already documented elsewhere.
  Always document critical constraints that could cause runtime issues, such as resource
  conflicts or usage limitations. Remove duplicate explanations that repeat information
  available in other parts of...
repository: browser-use/browser-use
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 69139
---

Configuration documentation should include all necessary constraints and limitations while avoiding redundant information that's already documented elsewhere. Always document critical constraints that could cause runtime issues, such as resource conflicts or usage limitations. Remove duplicate explanations that repeat information available in other parts of the documentation to maintain clarity and reduce verbosity.

Example of good constraint documentation:
```python
# Create browser config with user_data_dir
config = BrowserConfig(
    headless=False,
    user_data_dir="/path/to/your/user_data_dir"
)
```

The browser will use this directory to store all profile data, which will persist between browser sessions. Only one browser at a time can be running with this `user_data_dir`, make sure to close any browsers using it before starting `browser-use`.

Avoid duplicating parameter explanations that are already covered in function signatures or other documentation sections.