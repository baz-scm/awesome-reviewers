---
title: Consistent descriptive naming
description: 'Use clear, descriptive names that follow consistent patterns established
  in the codebase and broader programming standards. This includes:


  1. Choose unambiguous function names that clearly communicate purpose and behavior:'
repository: opencv/opencv
label: Naming Conventions
language: Other
comments_count: 10
repository_stars: 82865
---

Use clear, descriptive names that follow consistent patterns established in the codebase and broader programming standards. This includes:

1. Choose unambiguous function names that clearly communicate purpose and behavior:
```cpp
// Poor: Hard to understand what it does and how it differs from copyTo()
void overwriteTo(OutputArray m) const;

// Better: Clearer indication of behavior
void writeTo(OutputArray m) const;
```

2. Avoid unnecessary abbreviations when clarity would be improved:
```cpp
// Poor: Ambiguous abbreviation
CV_WRAP void computeCCM();

// Better: Clear meaning
CV_WRAP Mat computeColorCorrectionMatrix();
```

3. Use all capital letters with underscores for constants and enums:
```cpp
// Poor: Inconsistent capitalization
enum ColorCheckerType {
    COLORCHECKER_Macbeth,
    COLORCHECKER_Vinyl
};

// Better: Consistent all-caps for constants
enum ColorCheckerType {
    COLORCHECKER_MACBETH,
    COLORCHECKER_VINYL
};
```

4. Follow established naming patterns for related classes or components:
```cpp
// Poor: Inconsistent with existing naming patterns
enum DisposalMethod {
    GRFMT_GIF_Nothing = 0,
    GRFMT_GIF_PreviousImage = 1
};

// Better: Consistent naming pattern
enum GifDisposeMethod {
    GIF_DISPOSE_NONE = 1,
    GIF_DISPOSE_RESTORE_PREVIOUS = 3
};
```

5. Name setters with 'set' prefix for clarity:
```cpp
// Poor: Confusing whether this is getter or setter
int paletteSize(int setPaletteSize = 0);

// Better: Clear indication this is a setter
int setPaletteSize(int size);
```

This approach leads to more maintainable, readable, and self-documenting code while preserving consistency across the codebase.
