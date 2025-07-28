---
title: Explain documentation rationale
description: When writing user-facing documentation, always explain WHY a guideline
  or requirement exists, not just WHAT users should do. Users are more likely to follow
  instructions when they understand the reasoning behind them.
repository: hyprwm/Hyprland
label: Documentation
language: Yaml
comments_count: 2
repository_stars: 28863
---

When writing user-facing documentation, always explain WHY a guideline or requirement exists, not just WHAT users should do. Users are more likely to follow instructions when they understand the reasoning behind them.

Avoid "trust me bro" documentation that simply states rules without context. Instead, provide clear explanations of the problems that guidelines solve or the benefits they provide.

Example from issue templates:
```yaml
# Poor - just states the rule
description: Please attach log files instead of pasting them.

# Better - explains the reasoning  
description: When including text files (such as logs or config), please **always ATTACH** them, and not paste them directly. This is important because pasting text directly clutters the issue with unnecessary keywords, making github issue search useless.
```

This approach helps users understand the impact of their actions and leads to better compliance with documentation guidelines.