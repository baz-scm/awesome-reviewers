---
title: Cache expensive computations
description: Identify and cache the results of expensive operations that are computed
  repeatedly with the same inputs. This includes function calls, data structure creation,
  regex compilation, and complex calculations that don't change between invocations.
repository: microsoft/terminal
label: Performance Optimization
language: C++
comments_count: 8
repository_stars: 99242
---

Identify and cache the results of expensive operations that are computed repeatedly with the same inputs. This includes function calls, data structure creation, regex compilation, and complex calculations that don't change between invocations.

Common patterns to watch for:
- Repeated calls to the same expensive function with identical parameters
- Recreating the same data structures across multiple instances
- Recompiling regular expressions on each use
- Duplicate algorithmic work in related operations

Examples of optimization opportunities:

```cpp
// Before: Each CommandViewModel duplicates the same data
class CommandViewModel {
    IMap<ShortcutAction, hstring> _AvailableActionsAndNamesMap; // Duplicated across instances
};

// After: Share expensive data across instances
class CommandViewModel {
    static const IMap<ShortcutAction, hstring> _SharedActionsAndNames; // Computed once
};

// Before: Repeated expensive function calls
if (_WindowProperties.WindowName() != L"") {
    auto name = _WindowProperties.WindowName(); // Called again
}

// After: Cache the result
if (const auto windowName = _WindowProperties.WindowName(); !windowName.empty()) {
    // Use windowName variable
}

// Before: Regex compiled on every validation
void _validateRegex(const hstring& regex) {
    std::wregex{ regex.cbegin(), regex.cend() }; // Expensive compilation each time
}

// After: Cache compiled regex instances
static std::unordered_map<hstring, std::wregex> _regexCache;
```

This optimization is particularly important for operations in hot paths, UI updates, or when processing large datasets. Always measure performance impact to ensure the caching overhead doesn't exceed the benefits.