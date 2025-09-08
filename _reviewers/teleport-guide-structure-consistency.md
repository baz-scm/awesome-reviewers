---
title: Guide structure consistency
description: 'Documentation guides should follow a consistent structure and provide
  clear, descriptive content to improve user experience and comprehension.


  **Structure Requirements:**'
repository: gravitational/teleport
label: Documentation
language: Other
comments_count: 12
repository_stars: 19109
---

Documentation guides should follow a consistent structure and provide clear, descriptive content to improve user experience and comprehension.

**Structure Requirements:**
- Use standard how-to guide format: "How it works" section before Prerequisites, followed by numbered "Step X/Y" sections
- Use sentence case for headings (e.g., "Step 1/3. Configure Rancher access" not "Step 1/3. Configure Rancher Access")  
- Start with H2 headings, not H1 (title comes from frontmatter)
- Avoid multiple sets of "Step..." sections within a single guide - split into separate guides if needed

**Content Clarity:**
- Introduce code snippets with explanatory sentences before showing the code
- Provide concrete examples for configuration fields and their expected value types
- Include examples in context of YAML snippets rather than isolated fragments
- Be descriptive about precise fields users should enter rather than making them infer from examples

**Example:**
```yaml
# Configure the update schedule by defining groups and timing
kind: autoupdate_config
metadata:
  name: autoupdate-config
spec:
  agents:
    mode: enabled           # Enable automatic updates
    strategy: halt-on-error # Stop if any group fails
    schedules:
      regular:
        - name: development     # Group name (string)
          days: ["Mon","Tue"]   # Days of week (array)
          start_hour: 4         # UTC hour (0-23)
```

This approach reduces user confusion, maintains consistency across documentation, and provides the context needed for users to successfully complete tasks without guessing at requirements or structure.