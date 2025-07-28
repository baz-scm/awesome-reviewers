---
title: avoid redundant operations
description: 'Identify and eliminate unnecessary duplicate operations, redundant function
  calls, and repeated computations that can impact performance. Common patterns include:
  avoiding redundant parameter retrieval when values are already available, preventing
  duplicate map lookups by caching results, checking for changes before performing
  expensive operations, and...'
repository: electron/electron
label: Performance Optimization
language: Other
comments_count: 6
repository_stars: 117644
---

Identify and eliminate unnecessary duplicate operations, redundant function calls, and repeated computations that can impact performance. Common patterns include: avoiding redundant parameter retrieval when values are already available, preventing duplicate map lookups by caching results, checking for changes before performing expensive operations, and caching expensive computations for reuse.

Examples of optimization opportunities:
- Pass available parameters instead of recalculating: `UpdateWindowAccentColor(active)` rather than calling `IsActive()` again
- Cache map lookup results: `if (const auto* orig = base::FindOrNull(options.environment, key))` instead of separate `find()` and second lookup
- Guard expensive operations with change detection: `if (title == GetTitle()) return;` before triggering update events
- Cache expensive computations in static storage: `base::NoDestructor<std::string>` for values computed repeatedly during module loading
- Reuse V8 string objects: Create `v8::Local<v8::String>` keys once and reuse them instead of recreating identical strings multiple times

Consider debouncing rapidly-triggered operations like window state saves during resize events to prevent performance degradation from excessive I/O operations.