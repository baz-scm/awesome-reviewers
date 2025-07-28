---
title: Configuration documentation accuracy
description: Ensure configuration documentation is accurate, consistent, and clearly
  indicates optional versus required values. Use consistent terminology throughout
  documentation, provide accurate technical details, and make examples actionable
  for developers.
repository: alacritty/alacritty
label: Configurations
language: Other
comments_count: 5
repository_stars: 59675
---

Ensure configuration documentation is accurate, consistent, and clearly indicates optional versus required values. Use consistent terminology throughout documentation, provide accurate technical details, and make examples actionable for developers.

Key practices:
- Use consistent language when describing configuration behavior (e.g., "looks for" vs "should be located at")
- Accurately document default values and optional parameters, explicitly showing when values can be "None"
- Ensure technical details like Unicode ranges, data types, and formatting are correct
- Make examples directly usable by developers: "Every _Default:_ and _Example:_ entry is valid TOML and can be copied directly into the configuration file"
- Use proper formatting conventions consistently across all documentation

Example of good documentation structure:
```
*position* "None" | { x = <integer>, y = <integer> }

    Window startup position

    Specified in number of pixels.

    If the position is _"None"_, the window manager will handle placement.
    
    Default: _"None"_
```

This approach helps developers understand exactly what configuration options are available, what values are valid, and how to properly use them in their own configurations.