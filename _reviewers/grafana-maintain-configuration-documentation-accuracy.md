---
title: Maintain configuration documentation accuracy
description: 'Always ensure configuration documentation accurately reflects the current
  system capabilities, limitations, and feature availability status. When documenting
  configuration options:'
repository: grafana/grafana
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 68825
---

Always ensure configuration documentation accurately reflects the current system capabilities, limitations, and feature availability status. When documenting configuration options:

1. Regularly update documentation to remove or modify references to deprecated or changed configuration options
2. Clearly indicate feature availability status (GA, Public Preview, Experimental)
3. Provide precise descriptions of how configuration options affect system behavior
4. Don't document experimental features that aren't fully functional yet

Example:

```ini
# Incorrect (outdated) documentation
;footer_hide = true  # Use this to hide the footer

# Correct (updated) documentation
# footer_hide is no longer available
;footer_text = "Custom footer text"  # Set custom text for the footer
;footer_logo = "logo.png"  # Set custom logo for the footer
# If neither is set, the default Grafana footer is displayed
```

Accurate configuration documentation prevents user confusion, reduces support requests, and ensures smooth system operation across different environments.