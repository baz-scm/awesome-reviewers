---
title: Prefer safe optional handling
description: 'Always use Swift''s built-in mechanisms for safely handling optional
  values instead of force unwrapping or manual nil handling. Specifically:


  1. Use optional binding (`if let`, `guard let`) instead of checking for nil and
  force unwrapping:'
repository: ghostty-org/ghostty
label: Null Handling
language: Swift
comments_count: 3
repository_stars: 32864
---

Always use Swift's built-in mechanisms for safely handling optional values instead of force unwrapping or manual nil handling. Specifically:

1. Use optional binding (`if let`, `guard let`) instead of checking for nil and force unwrapping:

```swift
// Avoid this pattern
if savedWindowFrame != nil {
    let originalFrame = savedWindowFrame!  // Risky force unwrap
}

// Prefer this pattern
if let savedWindowFrame {
    let originalFrame = savedWindowFrame  // Safe access
}
```

2. Use collection transformation methods like `flatMap` or `compactMap` to handle optional collections elegantly:

```swift
// Avoid this pattern
return controllers.reduce([]) { result, c in
    result + (c.surfaceTree.root?.leaves() ?? [])
}

// Prefer this pattern
return controllers.flatMap {
    $0.surfaceTree.root?.leaves() ?? []
}
```

3. Always add appropriate guards to check if objects exist within expected hierarchies or collections before performing operations:

```swift
@IBAction func toggleMaximize(_ sender: Any) {
    guard let window = window else { return }
    guard surfaceTree.contains(sender) else { return }  // Check hierarchy membership
    // Implementation...
}
```

These patterns make code more concise, readable, and less prone to runtime crashes due to unexpected nil values.