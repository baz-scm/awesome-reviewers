---
title: Teach by example
description: Present concepts through clear, focused examples that demonstrate features
  positively rather than through comparisons or criticisms of alternative approaches.
  Allow readers to discover benefits through well-constructed examples rather than
  explicit statements about superiority.
repository: tensorflow/swift
label: Documentation
language: Other
comments_count: 5
repository_stars: 6136
---

Present concepts through clear, focused examples that demonstrate features positively rather than through comparisons or criticisms of alternative approaches. Allow readers to discover benefits through well-constructed examples rather than explicit statements about superiority.

For instance, instead of:

```swift
// OOP approaches have limitations because subclassing creates rigid hierarchies
```

Use an illustrative example:

```swift
// Here's how protocols allow for flexible composition
protocol Drawable {
    func draw()
}

struct Circle: Drawable {
    func draw() { /* implementation */ }
}

struct Square: Drawable {
    func draw() { /* implementation */ }
}

// Any type conforming to Drawable can be used here
func renderShapes(_ shapes: [Drawable]) {
    for shape in shapes {
        shape.draw()
    }
}
```

Keep examples simple and directly tied to the concept being taught. Complex examples with multiple concepts can confuse readers and obscure the main learning objective. When possible, make examples interactive so readers can experiment with the code and reach their own conclusions about its benefits.
