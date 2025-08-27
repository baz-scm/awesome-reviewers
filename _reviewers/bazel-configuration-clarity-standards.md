---
title: Configuration clarity standards
description: 'Configuration options should be designed with clarity, consistency,
  and user experience as primary concerns. This includes several key practices:


  **Clear and specific help text**: Flag descriptions should explicitly explain their
  purpose and scope to avoid user confusion. For example, instead of generic descriptions,
  be specific about when and how the flag...'
repository: bazelbuild/bazel
label: Configurations
language: Java
comments_count: 7
repository_stars: 24489
---

Configuration options should be designed with clarity, consistency, and user experience as primary concerns. This includes several key practices:

**Clear and specific help text**: Flag descriptions should explicitly explain their purpose and scope to avoid user confusion. For example, instead of generic descriptions, be specific about when and how the flag is used.

**Intuitive syntax with units**: When accepting time or quantity values, include units in the syntax for clarity. Use formats like `30s`, `5m`, `1h` instead of raw numbers, and document the expected format.

**Consistent behavioral patterns**: Maintain consistent conventions across similar flags. For example, if `0` disables functionality in some flags, apply this pattern consistently across related options. If `0` means "run immediately" for some flags, use the same convention for similar flags to reduce user confusion.

**Validation with helpful errors**: Prefer clear error messages over warnings for invalid configuration values. This reduces warning spam and makes it easier to evolve behavior later. Provide actionable feedback when validation fails.

**Proper option organization**: Place configuration options in appropriate option classes that reflect their actual usage and dependencies, rather than generic catch-all classes.

Example of good configuration design:
```java
@Option(
    name = "timeout",
    converter = DurationConverter.class,
    help = "Timeout for action execution. Use format like '30s', '5m', or '1h'. " +
           "Set to 0 to disable timeout.")
public Duration timeout;
```

This approach ensures configuration options are self-documenting, behave predictably, and provide a better developer experience.