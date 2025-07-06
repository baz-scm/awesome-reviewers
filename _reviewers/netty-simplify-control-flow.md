---
title: Simplify control flow
description: 'Streamline code by simplifying control flow structures to improve readability.
  Eliminate unnecessary nesting and verbosity by applying these guidelines:'
repository: netty/netty
label: Code Style
language: Java
comments_count: 7
repository_stars: 34227
---

Streamline code by simplifying control flow structures to improve readability. Eliminate unnecessary nesting and verbosity by applying these guidelines:

1. Remove redundant `else` blocks after `return`, `break`, `continue`, or `throw` statements:
```java
// Prefer this:
if (condition) {
    return value;
}
return otherValue;

// Over this:
if (condition) {
    return value;
} else {
    return otherValue;
}
```

2. Use early returns to reduce nesting levels:
```java
// Prefer this:
if (condition1) {
    // Handle special case
    return;
}
// Handle normal case

// Over this:
if (condition1) {
    // Handle special case
} else {
    // Handle normal case
}
```

3. Use concise conditional expressions for simple assignments:
```java
// Prefer this:
String scheme = ctx.pipeline().get(SslHandler.class) == null ? "http" : "https";

// Over this:
String scheme = "http";
if(ctx.channel().pipeline().get(SslHandler.class) != null) {
    scheme = "https";
}
```

4. Follow consistent loop patterns used throughout the codebase:
```java
// Use this pattern for polling loops:
for (;;) {
    Object msg = queue.poll();
    if (msg == null) {
        break;
    }
    pipeline.fireChannelRead(msg);
}

// Instead of while or other variations
```