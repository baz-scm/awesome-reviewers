---
title: Prevent regression crashes
description: When implementing error handling or bug fixes, avoid introducing new
  crash conditions that would break previously working code. Focus on defensive programming
  that handles edge cases without creating new failure points.
repository: facebook/react-native
label: Error Handling
language: Java
comments_count: 3
repository_stars: 123178
---

When implementing error handling or bug fixes, avoid introducing new crash conditions that would break previously working code. Focus on defensive programming that handles edge cases without creating new failure points.

Key principles:
1. **Backward compatibility first**: Don't add new validation that crashes on previously accepted inputs
2. **Complete error handling**: Ensure all code paths have proper error responses (like calling onResponseReceived for all URI handlers)
3. **Proper state management**: Reset and initialize state variables in lifecycle methods to prevent recycling issues

Example from accessibility handling:
```java
// DON'T: Add new crash conditions
if (!action.hasKey("name") || !action.hasKey("label")) {
  // This crashes apps that worked before without labels

// DO: Handle missing data gracefully  
if (!action.hasKey("name")) {
  continue; // Skip invalid actions without crashing
}
if (action.hasKey("label")) {
  // Use label when available, but don't require it
}
```

Before adding new error conditions, consider whether the change maintains backward compatibility while still providing proper error handling for new scenarios.