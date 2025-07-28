---
title: Keep documentation together
description: Documentation should keep related information physically close together
  rather than separating it across different sections. When documenting configuration
  options, provide detailed explanations and defaults directly with each option definition
  instead of collecting them in distant sections.
repository: alacritty/alacritty
label: Documentation
language: Other
comments_count: 2
repository_stars: 59675
---

Documentation should keep related information physically close together rather than separating it across different sections. When documenting configuration options, provide detailed explanations and defaults directly with each option definition instead of collecting them in distant sections.

Users should not have to scroll through large portions of documentation to find complete information about a single field. Each documented item should be self-contained with its description, possible values, platform restrictions, defaults, and examples all in proximity.

For example, instead of:
```
*level* = _"Normal"_ | _"AlwaysOnTop"_
    Sets the window level (Normal, AlwaysOnTop).
    Default: _"Normal"_
```

Provide detailed explanations:
```
*level* = _"Normal"_ | _"AlwaysOnTop"_
    Sets the window level.
    
    *Normal*
        Standard window behavior
    *AlwaysOnTop* 
        Window stays above other windows
        
    Default: _"Normal"_
```

This approach improves documentation usability by ensuring users can find complete information about any feature without extensive navigation, making the documentation more practical and user-friendly.