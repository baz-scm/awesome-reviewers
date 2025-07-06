---
title: Clear descriptive identifiers
description: Choose clear, self-descriptive names for all code identifiers that accurately
  reflect their purpose and behavior. Method names should be verbs or verb phrases
  that indicate their function without ambiguity. For boolean methods, use prefixes
  like "is", "has", or "should" followed by the condition they check.
repository: deeplearning4j/deeplearning4j
label: Naming Conventions
language: Java
comments_count: 3
repository_stars: 14036
---

Choose clear, self-descriptive names for all code identifiers that accurately reflect their purpose and behavior. Method names should be verbs or verb phrases that indicate their function without ambiguity. For boolean methods, use prefixes like "is", "has", or "should" followed by the condition they check.

When generating identifiers programmatically, use distinctive prefixes to avoid potential collisions with user-defined names. For example, prefer domain-specific prefixes like `sd_var_` over generic ones like `var_` to reduce collision risk.

```java
// Avoid:
public final static boolean gilIsReleaseAutomatically() {} // awkward phrasing, hard to parse
private void parseSetupAndExecCode() {} // ambiguous, could mean "parse setup and execute code"
String varName = "var_" + _var_id.toString(); // too generic prefix

// Prefer:
public final static boolean releaseGilAutomatically() {} // direct and clear
private void parseSetupAndExecutionCode() {} // clearer alternative
// or better with JavaDoc explaining the purpose
/**
 * Parses both the setup code and execution code sections from the configuration.
 */
private void parseCodeSections() {}
String varName = "sd_var_" + String.valueOf(_var_id); // domain-specific prefix
```

Meaningful naming reduces the need for comments, improves code readability, and makes the codebase more maintainable for all developers.