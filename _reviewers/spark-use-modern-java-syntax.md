---
title: use modern Java syntax
description: Prefer modern Java language features and constructs to write more concise,
  readable code. Since Apache Spark 4.0.0, the project recommends using contemporary
  Java syntax where applicable.
repository: apache/spark
label: Code Style
language: Java
comments_count: 3
repository_stars: 41554
---

Prefer modern Java language features and constructs to write more concise, readable code. Since Apache Spark 4.0.0, the project recommends using contemporary Java syntax where applicable.

Key practices:
- Use switch expressions (JEP-361) instead of traditional switch statements for cleaner, more compact code
- Use Java records for simple data structures instead of classes with boilerplate code
- Leverage pattern matching and other modern language features when appropriate

Examples:

**Switch expressions** - Replace verbose switch statements:
```java
// Instead of:
BloomFilter result;
switch (version) {
  case 1:
    result = BloomFilterImpl.readFrom(bin);
    break;
  case 2:
    result = BloomFilterImplV2.readFrom(bin);
    break;
  default:
    throw new IllegalArgumentException("Unknown BloomFilter version: " + version);
}
return result;

// Use:
return switch (version) {
  case 1 -> BloomFilterImpl.readFrom(bin);
  case 2 -> BloomFilterImplV2.readFrom(bin);
  default -> throw new IllegalArgumentException("Unknown BloomFilter version: " + version);
};
```

**Records for data structures** - Use records instead of classes for simple data holders:
```java
// Instead of a class with boilerplate:
public final class JoinColumn implements NamedReference {
  // constructor, getters, equals, hashCode, toString...
}

// Use a record:
public record JoinColumn(...) implements NamedReference {
  // automatic constructor, getters, equals, hashCode, toString
}
```

This approach reduces boilerplate code, improves readability, and takes advantage of language improvements that make code more maintainable.