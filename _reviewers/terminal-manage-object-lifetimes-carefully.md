---
title: manage object lifetimes carefully
description: Ensure proper object lifetime management in concurrent scenarios to prevent
  crashes from dangling pointers and premature destruction. Use weak references for
  event handlers that may outlive their target objects, and capture strong references
  in async operations to keep objects alive during coroutine execution.
repository: microsoft/terminal
label: Concurrency
language: C++
comments_count: 6
repository_stars: 99242
---

Ensure proper object lifetime management in concurrent scenarios to prevent crashes from dangling pointers and premature destruction. Use weak references for event handlers that may outlive their target objects, and capture strong references in async operations to keep objects alive during coroutine execution.

Key practices:
- Use `get_weak()` pattern for event handlers: `handler({ get_weak(), &Class::Method })` instead of raw `this` pointers
- Avoid leaving dangling event handlers with raw pointers when objects can be destroyed while events are still registered
- In coroutines, capture strong references to `this` when the object needs to stay alive across async boundaries: `auto strongThis = get_self<implementation::ClassName>();`
- Be cautious about background thread destruction - objects destroyed on background threads can break UI frameworks like WinUI

Example of proper weak reference usage:
```cpp
// Good: Uses weak reference pattern
_connection.StateChanged(winrt::auto_revoke, { get_weak(), &ControlCore::_connectionStateChangedHandler });

// Bad: Raw pointer that can dangle
_accessibilitySettings.HighContrastChanged([this](auto&&, auto&&) { 
    // 'this' may be destroyed while handler is still registered
});
```

This prevents race conditions where objects are destroyed while concurrent operations are still referencing them, which is a common source of crashes in multithreaded applications.