---
name: validate-nulls-properly-spring-boot
description: "Use appropriate null-check patterns in Spring (Java) code to avoid NullPointerExceptions and handle empty values correctly."
---

# Validate Nulls Properly (Spring Boot)

Null handling in Java is a common source of bugs. Spring Boot’s code reviews emphasize using the right utilities and patterns to handle nulls and empty values safely[47]:

- **Use Spring’s assertions for strings.** Instead of a generic null check on a `String`, use `Assert.hasText(str, "message")` (from Spring Framework) to ensure not only that the string is non-null but also not empty or whitespace[48]. This combines multiple checks in one and provides a clear error message if the assertion fails.
- **Check null before typecasting or comparison.** In `equals()` methods or other comparisons, always check the object is not null (and of the correct type) before accessing its methods or fields[49]. A typical pattern is:

```java
if (this == obj) return true;
if (obj == null || getClass() != obj.getClass()) return false;
// then safely cast and compare fields
```

This prevents `NullPointerException`s and ensures `equals` returns false for null or different types[49].
- **Validate collections are not null.** Before iterating or processing a collection (or array), verify it’s not null. Either use `CollectionUtils.isEmpty(collection)` to check, or guard with an `if (collection != null)` when appropriate[50]. If a collection can be null, consider initializing it to empty to simplify logic.
- **Prefer non-null defaults.** Where possible, design constructors or setters to default optional fields to empty collections or sensible defaults, so you avoid null checks altogether when using those objects[51].

By consistently applying these null-handling practices, Spring developers prevent a whole class of `NullPointerException` errors. The code becomes more robust and intention-revealing (e.g., using `hasText` clearly indicates we expect a non-blank string)[48].
