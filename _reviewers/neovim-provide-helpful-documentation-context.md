---
title: Provide helpful documentation context
description: Documentation should include sufficient context, practical examples,
  and helpful hints to make it truly useful for developers. Avoid assuming users have
  background knowledge - explain concepts, provide examples, and mention related functionality.
repository: neovim/neovim
label: Documentation
language: Txt
comments_count: 5
repository_stars: 91433
---

Documentation should include sufficient context, practical examples, and helpful hints to make it truly useful for developers. Avoid assuming users have background knowledge - explain concepts, provide examples, and mention related functionality.

Key practices:
- Explain technical terms and concepts (e.g., "what is a linked editing session?")
- Include practical examples and usage hints (e.g., "`:EditQuery <tab>` completes injected language names")
- Show command examples with common options (e.g., "+cmd examples for restart")
- Mention features in all relevant documentation locations, not just one place
- Ensure documentation positioning matches its actual complexity level

Example of good contextual documentation:
```
:restart[!] [+cmd]                                              *:restart*
    Restart Nvim. This fails when changes have been made. 
    Use :confirm restart to override.
    
    Examples:
        :restart +PluginUpdate    " Restart and run command
        :confirm restart          " Restart with change confirmation
```

This approach transforms documentation from mere reference material into genuinely helpful guidance that reduces the learning curve for users.