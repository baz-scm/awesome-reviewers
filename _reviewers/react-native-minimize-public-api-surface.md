---
title: minimize public API surface
description: Carefully evaluate whether functionality needs to be exposed as public
  API. Keep implementations private when they're only used internally, and avoid creating
  public APIs that increase maintenance burden without clear benefit.
repository: facebook/react-native
label: API
language: Other
comments_count: 4
repository_stars: 123178
---

Carefully evaluate whether functionality needs to be exposed as public API. Keep implementations private when they're only used internally, and avoid creating public APIs that increase maintenance burden without clear benefit.

Before exposing new public APIs, consider:
- Can the functionality be handled with existing patterns (e.g., platform checks in JavaScript instead of native module calls)?
- Is this API only used internally and can remain private?
- Are experimental APIs properly gated behind feature flags?
- Will adding parameters break API stability for existing callers?

Example from the codebase:
```objc
// Instead of exposing this in the header as public API:
RCT_EXTERN UIDeviceOrientation RCTDeviceOrientation(void);

// Keep it private in the .mm file since it's only used internally:
static UIDeviceOrientation RCTDeviceOrientation(void) {
  // implementation
}
```

For experimental features, use feature flags rather than exposing unstable APIs:
```objc
// Experimental APIs should be clearly marked and gated
textInputEventEmitter.experimental_flushSync([state = _state, data = std::move(data)]() mutable {
  // experimental functionality
});
```

This approach reduces maintenance overhead, prevents API bloat, and gives teams flexibility to refactor internal implementations without breaking public contracts.