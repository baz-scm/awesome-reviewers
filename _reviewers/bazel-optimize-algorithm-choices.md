---
title: optimize algorithm choices
description: Choose algorithms and data structures that provide both deterministic
  behavior and optimal performance characteristics. Prefer ordered collections when
  iteration order matters, optimize pattern matching to avoid expensive operations,
  and be mindful of algorithmic complexity.
repository: bazelbuild/bazel
label: Algorithms
language: Java
comments_count: 7
repository_stars: 24489
---

Choose algorithms and data structures that provide both deterministic behavior and optimal performance characteristics. Prefer ordered collections when iteration order matters, optimize pattern matching to avoid expensive operations, and be mindful of algorithmic complexity.

Key principles:
- Use deterministic data structures (e.g., `std::set` instead of `unsorted_set`, `ImmutableListMultimap` instead of custom maps) to ensure consistent output
- Optimize pattern matching by converting complex regex patterns to simpler string operations when possible: "If the pattern matches a literal suffix, optimize to a string suffix match, which is by far the fastest way to match"
- Preserve ordering semantics when filtering collections rather than treating them as unordered sets
- Avoid quadratic complexity algorithms, especially in scenarios with large N where "iterating over the packages and then over each mapping's entries would thus require time quadratic in N"
- Consider string containment (`indexOf`) over regex patterns for simple substring matching

Example optimization:
```java
// Instead of complex regex for simple suffix matching
if (LITERAL_PATTERN_WITH_DOT_UNESCAPED.matcher(suffixPattern).matches()) {
  String literalSuffix = suffixPattern.replace("\\.", ".");
  return s -> s.endsWith(literalSuffix);  // Much faster than regex
}

// Use ordered collections for deterministic behavior
ImmutableListMultimap<Label, SpawnStrategy> platformToStrategies;  // Preserves order
// Instead of: Map<Label, List<SpawnStrategy>>
```

This approach ensures both correctness through deterministic behavior and performance through algorithmic efficiency.