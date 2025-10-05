---
title: explicit code declarations
description: Always make code declarations explicit and consistent to improve readability
  and maintainability. This includes specifying all property attributes, using const
  for immutable parameters, and avoiding misleading naming conventions.
repository: facebook/yoga
label: Code Style
language: Other
comments_count: 4
repository_stars: 18255
---

Always make code declarations explicit and consistent to improve readability and maintainability. This includes specifying all property attributes, using const for immutable parameters, and avoiding misleading naming conventions.

Key practices:
- **Property attributes**: Explicitly specify all Objective-C property attributes instead of relying on defaults
- **Parameter constness**: Use const for function parameters that shouldn't be modified
- **Clear naming**: Avoid misleading prefixes like "g" (global) for member variables

Example of explicit property declaration:
```objc
// Good - explicit attributes
@property (nonatomic, readwrite, assign) CGFloat flexGrow;

// Avoid - relying on defaults
@property (nonatomic) CGFloat flexGrow;
```

Example of consistent const usage:
```c
// Good - const parameters
WIN_EXPORT void YGSetExperimentalFeatureEnabled(const YGConfigRef config,
                                                const YGExperimentalFeature feature,
                                                const bool enabled);

// Avoid - missing const
WIN_EXPORT void YGSetExperimentalFeatureEnabled(YGConfigRef config,
                                                YGExperimentalFeature feature,
                                                bool enabled);
```

This approach reduces ambiguity, makes code intentions clear, and helps prevent accidental modifications while improving overall code consistency.