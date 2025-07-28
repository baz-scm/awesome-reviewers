---
title: Maintain clean code structure
description: Keep code well-organized by separating interface from implementation,
  managing dependencies properly, and following consistent structural patterns. Function
  bodies should remain in implementation files rather than headers to reduce compilation
  dependencies and improve maintainability. Organize includes strategically - move
  them to implementation files when...
repository: hyprwm/Hyprland
label: Code Style
language: Other
comments_count: 8
repository_stars: 28863
---

Keep code well-organized by separating interface from implementation, managing dependencies properly, and following consistent structural patterns. Function bodies should remain in implementation files rather than headers to reduce compilation dependencies and improve maintainability. Organize includes strategically - move them to implementation files when possible and always use relative paths rather than src-based paths. Structure classes and functions appropriately by preferring namespaces over global functions, placing functions within relevant classes when they operate on class data, and following standard member ordering with private members last. Avoid unnecessary code elements like redundant `this` usage.

Example of proper structure:
```cpp
// Header file - interface only
class CHyprCtl {
public:
    static std::string getWindowData(PHLWINDOW w, eHyprCtlOutputFormat format);
private:
    // private members come last
    wl_event_source* m_eventSource = nullptr;
};

// Implementation file - bodies and includes
#include "relative/path/to/header.hpp"  // relative paths only
#include <fcntl.h>  // moved from global includes

std::string CHyprCtl::getWindowData(PHLWINDOW w, eHyprCtlOutputFormat format) {
    // implementation here, avoid unnecessary 'this->'
    return result;
}
```