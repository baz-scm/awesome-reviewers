---
title: Use null validation utilities
description: 'Consistently use utility methods like `ObjectUtil.checkNotNull()` or
  `Objects.requireNonNull()` to validate that parameters are not null. When assigning
  parameters to instance variables, combine the null check with the assignment for
  cleaner, more maintainable code:'
repository: netty/netty
label: Null Handling
language: Java
comments_count: 6
repository_stars: 34227
---

Consistently use utility methods like `ObjectUtil.checkNotNull()` or `Objects.requireNonNull()` to validate that parameters are not null. When assigning parameters to instance variables, combine the null check with the assignment for cleaner, more maintainable code:

```java
// Instead of:
public DohRecordEncoder(InetSocketAddress dohServer, boolean useHttpPost, String uri) {
    if (dohServer == null) {
        throw new NullPointerException("dohServer");
    }
    this.dohServer = dohServer;
    this.useHttpPost = useHttpPost;
    if (uri == null) {
        throw new NullPointerException("uri");
    }
    this.uri = uri;
}

// Do this:
public DohRecordEncoder(InetSocketAddress dohServer, boolean useHttpPost, String uri) {
    this.dohServer = ObjectUtil.checkNotNull(dohServer, "dohServer");
    this.useHttpPost = useHttpPost;
    this.uri = ObjectUtil.checkNotNull(uri, "uri");
}
```

This approach not only prevents NullPointerExceptions but also provides clear error messages, making debugging easier. For method parameters that should never be null, perform the check at the beginning of the method. When initializing components in a class, add appropriate null checks to the initialization or configuration methods rather than adding conditional null checks throughout the code.