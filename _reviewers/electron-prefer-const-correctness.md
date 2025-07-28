---
title: prefer const correctness
description: Always mark variables, parameters, and methods as `const` when they don't
  modify state. This improves code safety, enables compiler optimizations, and makes
  intent clearer to readers.
repository: electron/electron
label: Code Style
language: Other
comments_count: 7
repository_stars: 117644
---

Always mark variables, parameters, and methods as `const` when they don't modify state. This improves code safety, enables compiler optimizations, and makes intent clearer to readers.

Apply const in these scenarios:
- **Variables that don't change**: `const auto* command_line = base::CommandLine::ForCurrentProcess();`
- **Parameters that aren't modified**: `bool IsDetachedFrameHost(const content::RenderFrameHost* rfh)`
- **Methods that don't modify object state**: `bool IsWirelessSerialPortOnly() const;`
- **Pointers to immutable data**: `const display::Screen* screen = display::Screen::GetScreen();`

Example transformation:
```cpp
// Before
auto* command_line = base::CommandLine::ForCurrentProcess();
display::Screen* screen = display::Screen::GetScreen();
bool IsDetachedFrameHost(content::RenderFrameHost* rfh);

// After  
const auto* command_line = base::CommandLine::ForCurrentProcess();
const display::Screen* screen = display::Screen::GetScreen();
bool IsDetachedFrameHost(const content::RenderFrameHost* rfh);
```

Const correctness prevents accidental modifications, enables the compiler to catch errors early, and serves as documentation of your code's intent. When in doubt, start with const and remove it only if modification is necessary.