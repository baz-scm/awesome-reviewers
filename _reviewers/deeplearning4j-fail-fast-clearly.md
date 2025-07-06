---
title: Fail fast clearly
description: Detect and report errors as early as possible with detailed context to
  prevent silent failures and aid debugging. Validate inputs, states, and implementation
  completeness with appropriate exceptions that include relevant information.
repository: deeplearning4j/deeplearning4j
label: Error Handling
language: Java
comments_count: 4
repository_stars: 14036
---

Detect and report errors as early as possible with detailed context to prevent silent failures and aid debugging. Validate inputs, states, and implementation completeness with appropriate exceptions that include relevant information.

Key practices:
1. Validate parameters with explicit checks rather than silently ignoring invalid values:

```java
// AVOID: Silently ignoring invalid parameters
if (gamma > 0)
    this.gamma = gamma;
// Negative gamma silently ignored

// PREFER: Explicit validation with informative errors
Preconditions.checkArgument(gamma > 0, 
    "Gamma must be positive, got %s", gamma);
this.gamma = gamma;
```

2. Include relevant context in error messages to facilitate debugging:

```java
// AVOID: Generic errors without context
if (shape[dimension] != 1) {
    throw new ND4JIllegalStateException("Can squeeze only dimensions of size 1.");
}

// PREFER: Detailed exceptions with context
Preconditions.checkState(shape[dimension] == 1,
    "Can squeeze only dimensions of size 1. Dimension %s has size %s. Shape: %s", 
    dimension, shape[dimension], Arrays.toString(shape));
```

3. Use efficient validation patterns that avoid unnecessary object creation:

```java
// AVOID: Always constructing error messages
Preconditions.checkState(input.shape().length == 3,
    "3D input expected to RNN layer expected, got " + input.shape().length);

// PREFER: Lazy message construction with format strings
Preconditions.checkState(input.rank() == 3, 
    "3D input expected to RNN layer, got %s", input.rank());
```

4. For unimplemented functionality, throw clear exceptions rather than allowing silent failures:

```java
// AVOID: Unimplemented code with TODOs
if (modelParamsSupplier != null) {
    val params = modelParamsSupplier.get();
    if (params != null) {
        // TODO: We should propagate params across the workers
    }
}

// PREFER: Throw exception for unimplemented functionality
if (modelParamsSupplier != null) {
    val params = modelParamsSupplier.get();
    if (params != null) {
        throw new UnsupportedOperationException(
            "Parameter propagation to workers not yet implemented");
    }
}
```