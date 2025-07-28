---
title: Algorithm selection correctness
description: Choose algorithms that correctly match the problem requirements and understand
  their computational properties and side effects. Avoid using overly general solutions
  (like regex) when simpler, more precise algorithms exist.
repository: evanw/esbuild
label: Algorithms
language: Go
comments_count: 4
repository_stars: 39161
---

Choose algorithms that correctly match the problem requirements and understand their computational properties and side effects. Avoid using overly general solutions (like regex) when simpler, more precise algorithms exist.

Key principles:
1. **Match algorithm to problem domain**: Use domain-specific algorithms rather than general-purpose ones when precision matters. For example, TypeScript path mapping requires prefix/suffix matching, not regex pattern matching.

2. **Understand algorithmic side effects**: Operations like `p.findSymbol` may have side effects (marking usage) that affect other parts of the system. Document and account for these effects.

3. **Centralize complex algorithmic logic**: Place intricate algorithms like collision resolution in dedicated, well-audited locations rather than scattering the complexity across multiple passes.

Example of incorrect algorithm selection:
```go
// Incorrect: Using regex for simple pattern matching
if matched, err := regexp.MatchString("^"+key, path); matched && err == nil {
    // This treats '*' as regex repetition, not literal asterisk
}

// Correct: Use prefix/suffix matching like TypeScript compiler
func isPatternMatch(prefix, suffix, candidate string) bool {
    return len(candidate) >= len(prefix) + len(suffix) &&
           strings.HasPrefix(candidate, prefix) &&
           strings.HasSuffix(candidate, suffix)
}
```

Before implementing an algorithm, verify it handles edge cases correctly and matches the computational complexity requirements of your use case.