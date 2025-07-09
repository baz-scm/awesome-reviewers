---
title: Documentation clarity and formatting
description: 'Ensure documentation is clear, precise, and consistently formatted.
  Key practices include:


  1. **Be explicit and unambiguous** - Define terms that might be unclear and provide
  specific guidance:'
repository: ghostty-org/ghostty
label: Documentation
language: Yaml
comments_count: 8
repository_stars: 32864
---

Ensure documentation is clear, precise, and consistently formatted. Key practices include:

1. **Be explicit and unambiguous** - Define terms that might be unclear and provide specific guidance:
   ```
   // Instead of:
   Please provide the minimum configuration needed.
   
   // Use:
   Please provide the minimum configuration needed to reproduce this issue. If you can still reproduce the issue with one of the lines removed, do not include that line.
   ```

2. **Use consistent naming and capitalization** for UI elements - Be precise about component names and locations:
   ```
   // Instead of:
   Screenshot of the terminal inspector's logged keystrokes
   
   // Use:
   Screenshot of logged keystrokes from the terminal inspector's "Keyboard" tab
   ```

3. **Format code examples properly** - Always wrap code and configuration examples in markdown code blocks with triple backticks, and include version information where relevant:
   ```markdown
   #### `tmux.conf` (tmux 3.5a)
   ```
   set -g default-terminal "tmux-256color"
   set-option -sa terminal-overrides ",xterm*:Tc"
   ```
   ```

4. **Provide platform-specific instructions** when behavior differs between environments:
   ```
   // Instead of:
   Provide any captured Ghostty logs.
   
   // Use:
   Provide any captured Ghostty logs. On Linux, this can be found by running `ghostty` from the command-line; on macOS, this can be found via [specific instructions].
   ```

5. **Use present tense** for examples and descriptions rather than future tense.