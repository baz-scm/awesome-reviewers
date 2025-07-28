---
title: platform API consistency
description: When implementing cross-platform functionality, prioritize consistency
  and avoid replicating platform-specific bugs or inconsistencies. Consider the broader
  architectural impact of API choices, especially when they require significant migrations
  or affect multiple components.
repository: facebook/react-native
label: Networking
language: Java
comments_count: 2
repository_stars: 123178
---

When implementing cross-platform functionality, prioritize consistency and avoid replicating platform-specific bugs or inconsistencies. Consider the broader architectural impact of API choices, especially when they require significant migrations or affect multiple components.

For example, when choosing between platform-specific APIs (like AndroidX ComponentActivity.enableEdgeToEdge()) versus custom implementations, evaluate:
- Migration scope and complexity across the codebase
- Consistency requirements across different UI contexts (Activities, Dialogs, Modals)
- Whether platform-specific behaviors should be replicated or corrected

```java
// Avoid replicating iOS bugs for the sake of parity
if (data.mAnimated) {
  scrollView.reactSmoothScrollTo(data.mDestX, data.mDestY);
  scrollView.handleSmoothScrollMomentumEvents(); // Only for animated scrolls
} else {
  scrollView.scrollTo(data.mDestX, data.mDestY);
  // Don't emit momentum events for non-animated scrolls
}
```

Note: These discussions focus on UI/platform concerns rather than networking protocols, which suggests a category mismatch in the analysis request.