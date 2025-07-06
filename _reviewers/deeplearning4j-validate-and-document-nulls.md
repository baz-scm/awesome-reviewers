---
title: Validate and document nulls
description: 'Always handle null values explicitly and consistently throughout your
  codebase to prevent null pointer exceptions. Follow these guidelines:


  1. **Validate nulls early** using Preconditions to provide clear error messages:'
repository: deeplearning4j/deeplearning4j
label: Null Handling
language: Java
comments_count: 6
repository_stars: 14036
---

Always handle null values explicitly and consistently throughout your codebase to prevent null pointer exceptions. Follow these guidelines:

1. **Validate nulls early** using Preconditions to provide clear error messages:

```java
// Use explicit null checks with informative messages
Preconditions.checkNotNull(input, "Input cannot be null");
Preconditions.checkArgument(shape != null && shape.length > 0, "Invalid shape: %s", shape);
```

2. **Document null behavior** clearly in Javadoc comments:

```java
/**
 * Creates a buffer in the specified workspace.
 * @param workspace Optional memory workspace to define the buffer in, may be null 
 *                 (buffer not created in workspace when null)
 */
public DataBuffer createBuffer(DataType dataType, long length, boolean initialize, MemoryWorkspace workspace) {
    // Implementation
}
```

3. **Handle nulls at the source** rather than requiring downstream methods to handle them, preventing defensive null checks throughout the codebase.

4. **Use appropriate types** for potentially null values from collections:
```java
// Instead of:
int numWords = (int) tokenizerConfig.get("num_words");
// Use:
Integer numWords = (Integer) tokenizerConfig.get("num_words");
```

5. **Consider using annotations** like `@NonNull` or `@Nullable` to clearly indicate intent and enable static analysis tools to catch potential null issues.

Following these practices helps prevent null pointer exceptions and makes code more robust and maintainable.