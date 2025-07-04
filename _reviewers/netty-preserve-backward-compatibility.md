---
title: Preserve backward compatibility
description: 'When evolving APIs in minor versions, always maintain backward compatibility
  to avoid breaking client code. Follow these principles:


  1. **Don''t add abstract methods** to existing interfaces or abstract classes. Instead,
  provide default implementations:'
repository: netty/netty
label: API
language: Java
comments_count: 4
repository_stars: 34227
---

When evolving APIs in minor versions, always maintain backward compatibility to avoid breaking client code. Follow these principles:

1. **Don't add abstract methods** to existing interfaces or abstract classes. Instead, provide default implementations:

```java
// AVOID (breaking change):
public interface EventExecutorGroup {
    long submittedTasks(); // New abstract method breaks implementing classes
}

// BETTER:
public interface EventExecutorGroup {
    // Default implementation preserves compatibility
    default long submittedTasks() {
        return -1; // Indicates metric not supported
    }
}
```

2. **Implement missing abstract methods** when adding them to existing classes:

```java
// AVOID (breaking change):
public abstract String readString(int length, Charset charset);

// BETTER:
public String readString(int length, Charset charset) {
    String string = toString(readerIndex(), length, charset);
    skipBytes(length);
    return string;
}
```

3. **Deprecate methods before removing** them in major versions, with clear migration paths:

```java
@Deprecated
public static ZlibDecoder newZlibDecoder() {
    return newZlibDecoder(0); // Forward to newer method
}

public static ZlibDecoder newZlibDecoder(int maxAllocation) {
    // New implementation with additional parameter
}
```

4. **Maintain consistent deprecation** across related methods, constructors, and classes. When deprecating a method, also deprecate related methods and constructors that would become inconsistent.

Following these principles ensures your API evolves cleanly without disrupting existing users, allowing them to migrate at their own pace.