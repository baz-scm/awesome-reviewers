---
title: Prefer Readable Conditionals
description: 'When updating or adding code, keep control flow and non-trivial expressions
  easy to reason about.


  Rules of thumb:

  - Avoid nested ternary operators; use `switch` (or equivalent) for branching decisions.'
repository: apple/container
label: Code Style
language: Swift
comments_count: 5
repository_stars: 48787
---

When updating or adding code, keep control flow and non-trivial expressions easy to reason about.

Rules of thumb:
- Avoid nested ternary operators; use `switch` (or equivalent) for branching decisions.
- For multi-step math/logic, avoid “one-line” expressions. Extract intermediate results into named `let` constants (and keep comments aligned with the computation).
- Minimize mutable state inside functions—prefer `let` bindings and explicit, branch-local variables.
- If multiple sites need the same formatting/config/argument parsing logic, centralize it in a helper to keep behavior consistent and the code easier to read.

Example (turning a hard-to-read expression into named values):
```swift
// Before: hard to reason about clamp in a single line
let barLength = min(remainingWidth, max(0, state.finished ? remainingWidth : Int(Int64(remainingWidth) * value / total)))

// After: readable intermediate values
let reservedWidth = (useColor ? joinedComponents.visibleLength : joinedComponents.count) + 45
let completedBarWidth = max(config.width - usedWidth, 1)
let progressWidth = max(0, Int(Int64(completedBarWidth) * value / total))
let currentBarWidth: Int = state.finished ? completedBarWidth : min(completedBarWidth, progressWidth)
let barLength = min(remainingWidth, currentBarWidth)
```

Example (avoiding nested ternary):
```swift
switch progress {
case .plain:
    outputMode = .plain
case .color:
    outputMode = .color
default:
    outputMode = .ansi
}
```

Apply this during code review to make future changes safer and faster.