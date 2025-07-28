---
title: Document configuration specifics
description: When documenting configuration options in changelogs, README files, or
  other user-facing documentation, focus on specific implementation details and user-actionable
  information rather than vague feature descriptions. Write from the user's perspective,
  specifying exact configuration keys, values, and behaviors.
repository: alacritty/alacritty
label: Configurations
language: Markdown
comments_count: 7
repository_stars: 59675
---

When documenting configuration options in changelogs, README files, or other user-facing documentation, focus on specific implementation details and user-actionable information rather than vague feature descriptions. Write from the user's perspective, specifying exact configuration keys, values, and behaviors.

Key principles:
- Include actual config option names and example values
- Describe what the user will experience, not internal implementation details
- Use precise, implementation-specific language over generic descriptions
- Focus on user benefits and practical usage

Examples:
- Instead of: "Add additional fallback under `/etc/alacritty/alacritty.toml` for system wide configuration"
- Write: "Add `/etc/alacritty/alacritty.toml` fallback for system wide configuration"

- Instead of: "Shell initialization on macOS to manually check the `~/.hushlogin` file"  
- Write: "Pass `-q` to `login` on macOS if `~/.hushlogin` is present"

- Instead of: "window.level sets preferred window level (Normal, AlwaysOnTop)"
- Write: "Config option `window.level = "AlwaysOnTop"` to force Alacritty to always be the toplevel window"

Remember: "We don't document things for developers, we document them for users." Configuration documentation should help users understand exactly what to configure and what behavior to expect.