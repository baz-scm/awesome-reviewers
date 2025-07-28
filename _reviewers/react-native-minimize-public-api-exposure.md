---
title: minimize public API exposure
description: Keep internal implementation details private to reduce security attack
  surface. Public properties in header files can be accessed and potentially manipulated
  by external code, creating security vulnerabilities. Store internal state using
  private instance variables in the implementation file instead of exposing them through
  public properties.
repository: facebook/react-native
label: Security
language: Other
comments_count: 1
repository_stars: 123178
---

Keep internal implementation details private to reduce security attack surface. Public properties in header files can be accessed and potentially manipulated by external code, creating security vulnerabilities. Store internal state using private instance variables in the implementation file instead of exposing them through public properties.

Example of the security issue:
```objc
// ❌ Bad - exposes internal state publicly
@property (nonatomic, assign) BOOL isFirstRender;
@property (nonatomic, strong) NSArray<UIBarButtonItemGroup *> *initialValueLeadingBarButtonGroups;
```

Secure alternative:
```objc
// ✅ Good - keep internal state private
@implementation ClassName {
    BOOL isFirstRender;
    NSArray<UIBarButtonItemGroup *> *initialValueLeadingBarButtonGroups;
}
```

This follows the principle of least privilege by only exposing what external consumers actually need to access, reducing the potential for security exploits through API misuse.