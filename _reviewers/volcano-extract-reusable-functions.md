---
title: Extract reusable functions
description: When you identify duplicate code blocks, complex logic that can be simplified,
  or functionality that doesn't belong in its current location, extract it into well-named,
  reusable functions. This improves code organization, reduces duplication, and enhances
  readability.
repository: volcano-sh/volcano
label: Code Style
language: Go
comments_count: 9
repository_stars: 4899
---

When you identify duplicate code blocks, complex logic that can be simplified, or functionality that doesn't belong in its current location, extract it into well-named, reusable functions. This improves code organization, reduces duplication, and enhances readability.

Key scenarios to apply this practice:
- **Duplicate code**: Extract common logic into shared functions (e.g., "L397-L410 is the same as in normalPreempt L277-L285, I think we can extract a public func")
- **Complex conditionals**: Break down nested if statements into descriptive helper functions (e.g., "Better abstract a function here like jobTerminated to increase code readability")
- **Misplaced functionality**: Move functions to appropriate modules based on their responsibility (e.g., "can we move to util.go? This method does not seem to be directly related to session")
- **Validation logic**: Separate validation concerns into focused functions (e.g., "It is best to extract a function that validate memberType separately, otherwise the responsibility of the func validateHyperNodeMemberSelector does not match")

Example transformation:
```go
// Before: Complex inline logic
if req.Event != busv1alpha1.PodPendingEvent {
    cc.delayActionMapLock.Lock()
    if taskMap, exists := cc.delayActionMap[key]; exists {
        for podName, delayAct := range taskMap {
            // 20+ lines of complex cancellation logic
        }
    }
    cc.delayActionMapLock.Unlock()
}

// After: Extracted function
if req.Event != busv1alpha1.PodPendingEvent {
    cc.cancelDelayedActions(key, req)
}

func (cc *jobcontroller) cancelDelayedActions(key string, req *Request) {
    cc.delayActionMapLock.Lock()
    defer cc.delayActionMapLock.Unlock()
    // Clear, focused cancellation logic
}
```

This practice makes code more maintainable, testable, and easier to understand by giving complex operations descriptive names and clear boundaries.