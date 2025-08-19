---
title: Implement defensive validation
description: Always validate inputs, check boundaries, and avoid relying on undocumented
  API behavior or assumptions about how functions handle edge cases. When dealing
  with potentially null or invalid data, implement explicit checks rather than assuming
  the API will behave consistently across all scenarios.
repository: microsoft/terminal
label: Error Handling
language: C++
comments_count: 4
repository_stars: 99242
---

Always validate inputs, check boundaries, and avoid relying on undocumented API behavior or assumptions about how functions handle edge cases. When dealing with potentially null or invalid data, implement explicit checks rather than assuming the API will behave consistently across all scenarios.

Key practices:
- Don't assume APIs preserve or destroy values on failure - use fallback values instead
- Validate parameters before passing them to functions, especially when null could cause issues
- Check array/buffer boundaries before accessing elements
- Skip or handle invalid entries gracefully rather than processing them blindly

Example from the codebase:
```cpp
// Instead of assuming SystemParametersInfoW preserves the value on failure
unsigned int hoverTimeoutMillis{ 400 };
if (FAILED(SystemParametersInfoW(SPI_GETMOUSEHOVERTIME, 0, &hoverTimeoutMillis, 0)))
{
    hoverTimeoutMillis = 400; // Explicit fallback value
}

// Validate before processing
if (!settingsModelEntries)
{
    return single_threaded_observable_vector<Editor::NewTabMenuEntryViewModel>(std::move(result));
}

// Check boundaries to prevent crashes
if (iter.Pos() < _selection->start || iter.Pos() > _selection->end)
{
    // Safe to proceed with operation
}
```

This approach prevents crashes, undefined behavior, and makes code more robust by not relying on implementation details that may change or vary across different environments.