---
title: Defensive null validation
description: Always validate null parameters and dependencies early with proper ordering
  to prevent NullPointerExceptions and provide clear error messages. Use defensive
  programming practices including parameter validation, method overloading instead
  of null parameter handling, and careful ordering of null checks.
repository: apache/kafka
label: Null Handling
language: Java
comments_count: 5
repository_stars: 30575
---

Always validate null parameters and dependencies early with proper ordering to prevent NullPointerExceptions and provide clear error messages. Use defensive programming practices including parameter validation, method overloading instead of null parameter handling, and careful ordering of null checks.

Key practices:
1. **Early parameter validation**: Check for null parameters at method entry points using `Objects.requireNonNull()` with descriptive messages
2. **Proper validation ordering**: Perform null checks before operations that could mask the real cause of NPEs
3. **Method overloading over null handling**: Instead of accepting null parameters and checking them, provide separate method signatures
4. **Proactive dependency checking**: Validate that required dependencies exist before using them to avoid runtime NPEs

Example of proper null validation ordering:
```java
public record CommittedPartitionState(Set<Integer> isr, LeaderRecoveryState leaderRecoveryState) {
    public CommittedPartitionState {
        Objects.requireNonNull(isr); // Check null first
        this.isr = Set.copyOf(isr);   // Then perform operations
        Objects.requireNonNull(leaderRecoveryState);
    }
}
```

Example of method overloading instead of null checks:
```java
// Instead of: props(Properties extraProperties) with null check
private Properties props() { /* base implementation */ }
private Properties props(Properties extraProperties) {
    Properties config = props();
    config.putAll(extraProperties); // No null check needed
    return config;
}
```

This approach prevents NPEs, provides clearer stack traces when failures occur, and makes the code's null-handling contract explicit to callers.