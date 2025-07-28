---
title: Follow existing naming conventions
description: When adding new variables, methods, or constants, always follow the naming
  conventions already established in the codebase. Before introducing new identifiers,
  examine existing code in the same file and related files to understand the established
  patterns, including prefixes, suffixes, and naming styles.
repository: facebook/react-native
label: Naming Conventions
language: Java
comments_count: 2
repository_stars: 123178
---

When adding new variables, methods, or constants, always follow the naming conventions already established in the codebase. Before introducing new identifiers, examine existing code in the same file and related files to understand the established patterns, including prefixes, suffixes, and naming styles.

For example, when adding boolean fields to a class that uses 'm' prefixes and 'Did' prefixes for state variables, maintain consistency:

```java
// Existing code shows the pattern:
private boolean mContextMenuHidden = false;
private boolean mDidAttachToWindow = false;
private boolean mSelectTextOnFocus = false;

// Follow the established convention:
private boolean mDidSelectTextOnFocus = false;  // ✓ Correct

// Rather than breaking the pattern:
private boolean hasSelectedTextOnFocus = false;  // ✗ Inconsistent
```

This applies to all identifiers including constants, where numbering and naming should be synchronized across related files to maintain architectural consistency. Consistent naming conventions improve code readability, reduce cognitive load, and make the codebase easier to maintain.