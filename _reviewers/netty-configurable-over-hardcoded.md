---
title: Configurable over hardcoded
description: 'Make configuration parameters configurable rather than hardcoding values,
  especially for limits, sizes, and thresholds. Provide reasonable defaults but allow
  users to override through:'
repository: netty/netty
label: Configurations
language: Java
comments_count: 4
repository_stars: 34227
---

Make configuration parameters configurable rather than hardcoding values, especially for limits, sizes, and thresholds. Provide reasonable defaults but allow users to override through:

1. Constructor parameters for instance-specific configuration
2. System properties for application-wide defaults
3. Public accessor methods for runtime feature detection

For related configuration parameters, design APIs that ensure they are set cohesively to prevent invalid states:

```java
// Prefer this:
public IoUringIoHandlerConfig setSize(int ringSize, int cqSize) {
    // validate interdependent parameters together
    return this;
}

// Over separate methods that could create invalid configurations:
public IoUringIoHandlerConfig setRingSize(int ringSize) { ... }
public IoUringIoHandlerConfig setCqSize(int cqSize) { ... }
```

When exposing configuration capabilities, make feature detection methods public to help users adapt to different environments:

```java
if (IoUring.isRecvMultishotEnabled()) {
    // Use optimized configuration
}
```

Size-related parameters should be derived from existing configurations when reasonable rather than using arbitrary hardcoded values.