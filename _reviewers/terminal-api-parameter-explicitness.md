---
title: API parameter explicitness
description: Always use correct and explicit parameters when calling APIs, rather
  than relying on defaults or passing incorrect values. This includes passing appropriate
  objects to API methods, specifying all required parameters explicitly, and using
  correct operation patterns.
repository: microsoft/terminal
label: API
language: C++
comments_count: 4
repository_stars: 99242
---

Always use correct and explicit parameters when calling APIs, rather than relying on defaults or passing incorrect values. This includes passing appropriate objects to API methods, specifying all required parameters explicitly, and using correct operation patterns.

Key practices:
- Pass the correct object references to API methods (e.g., `nullptr` instead of `*this` when documentation suggests it)
- Always provide explicit parameters for programmatic operations, especially when dealing with external tools or services
- Use proper operation patterns (e.g., pre-increment `--iterator` when you don't need the previous result)
- Prefer efficient API methods when available (e.g., `ReplaceAll()` instead of `Clear()` followed by multiple `Append()` calls)

Example from the codebase:
```cpp
// Instead of passing potentially incorrect object reference
eventArgs.GetCurrentPoint(*this).Properties().IsMiddleButtonPressed()

// Pass the correct parameter as documented
eventArgs.GetCurrentPoint(nullptr).Properties().IsMiddleButtonPressed()

// For programmatic operations, always specify explicit parameters
profile->Commandline(winrt::hstring{ 
    fmt::format(FMT_COMPILE(L"cmd /k winget install --interactive --id Microsoft.PowerShell --source winget & echo. & echo {} & exit"), 
    RS_(L"PowerShellInstallationInstallerGuidance")) 
});
```

This approach reduces bugs, improves maintainability, and ensures APIs behave as intended rather than relying on potentially fragile default behaviors.