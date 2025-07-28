---
title: Follow platform naming conventions
description: Adhere to the established naming conventions and namespacing practices
  of your target platform. This includes following language-specific patterns for
  method names, avoiding namespace pollution in headers, and properly namespacing
  exported functions.
repository: facebook/react-native
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 123178
---

Adhere to the established naming conventions and namespacing practices of your target platform. This includes following language-specific patterns for method names, avoiding namespace pollution in headers, and properly namespacing exported functions.

For Objective-C:
- Methods prefixed with `get` should return results via pointer arguments, not return values directly
- Exported functions should include appropriate prefixes (e.g., `RCT` prefix)
- Avoid `using namespace` declarations in header files to prevent namespace pollution

Example violations and fixes:
```objc
// ❌ Violates Objective-C naming convention
+ (std::pair<CGPoint, CGPoint>)getPointsForCAGradientLayerLinearGradient:(CGPoint)startPoint

// ✅ Follows convention by removing 'get' prefix
+ (std::pair<CGPoint, CGPoint>)pointsForCAGradientLayerLinearGradient:(CGPoint)startPoint

// ❌ Missing namespace prefix for exported function
RCT_EXTERN RCTFontWeight weightOfFont(UIFont *font);

// ✅ Properly namespaced
RCT_EXTERN RCTFontWeight RCTGetFontWeight(UIFont *font);
```

Platform naming conventions exist for good reasons - they improve code readability, prevent naming conflicts, and ensure consistency with the broader ecosystem.