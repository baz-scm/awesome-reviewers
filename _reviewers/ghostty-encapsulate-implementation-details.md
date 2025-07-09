---
title: Encapsulate implementation details
description: When designing APIs, create appropriate abstractions that hide platform-specific
  or low-level implementation details from consuming code. Avoid exposing raw interfaces
  outside their designated modules and minimize unnecessary dependencies.
repository: ghostty-org/ghostty
label: API
language: Other
comments_count: 3
repository_stars: 32864
---

When designing APIs, create appropriate abstractions that hide platform-specific or low-level implementation details from consuming code. Avoid exposing raw interfaces outside their designated modules and minimize unnecessary dependencies.

**Good Practice:**
- Isolate platform-specific code in dedicated modules
- Use abstractions that hide underlying implementation complexity
- Only bind to resources that are actually used
- Consider direct imports for external dependencies when appropriate

For example, instead of binding to an unused protocol:

```zig
// AVOID: Unnecessary binding that adds dependencies
if (registryBind(
    xdg.WmDialogV1,
    registry,
    global,
)) |wm_dialog| {
    context.xdg_wm_dialog = wm_dialog;
    return;
}
```

Instead, simply check if the protocol is available without binding:

```zig
// BETTER: Just compare against the name and set a flag
if (isProtocolSupported(registry, global, "xdg_wm_dialog")) {
    context.has_wm_dialog_support = true;
    return;
}
```

Similarly, avoid using raw C interfaces outside their dedicated modules. Create proper abstractions that isolate platform-specific details, making the codebase more maintainable and portable.