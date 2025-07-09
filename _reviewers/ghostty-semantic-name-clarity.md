---
title: Semantic name clarity
description: 'Names should clearly and accurately reflect the purpose of variables,
  methods, and other identifiers. Follow these principles:


  1. Use descriptive, specific names that convey exact purpose'
repository: ghostty-org/ghostty
label: Naming Conventions
language: Swift
comments_count: 4
repository_stars: 32864
---

Names should clearly and accurately reflect the purpose of variables, methods, and other identifiers. Follow these principles:

1. Use descriptive, specific names that convey exact purpose
2. For booleans, prefer positive phrasing with 'is' prefix when appropriate
3. Update names when functionality changes
4. Follow established platform conventions (e.g., AppKit notification naming patterns)

**Example 1:** Instead of:
```swift
var macosHidden: Bool
```
Use:
```swift
var isAppIconHiddenFromMacOS: Bool
```

**Example 2:** When a function's responsibility expands:
```swift
// Before: only hides elements
func hideCustomTabBarViews() {
    // hide some elements
}

// After: both hides and shows elements
func resetCustomTabBarViews() {
    // hide some elements
    // show other elements
}
```

**Example 3:** For notification naming, follow consistent patterns:
```swift
// Avoid inconsistent patterns
static let ghosttyToggleMaximize = Notification.Name(...)

// Follow "[Subject] [Event (past participle)]" pattern
static let ghosttyFullscreenDidToggle = Notification.Name(...)
```