---
title: Optimize test case design
description: 'Write focused, efficient tests that validate core functionality without
  unnecessary complexity. Key principles:


  1. Test one concept per case

  2. Use appropriate test scope (unit vs integration)'
repository: spring-projects/spring-boot
label: Testing
language: Java
comments_count: 8
repository_stars: 77637
---

Write focused, efficient tests that validate core functionality without unnecessary complexity. Key principles:

1. Test one concept per case
2. Use appropriate test scope (unit vs integration)
3. Leverage modern testing tools

Instead of exhaustive parameterized tests:

```java
@ParameterizedTest
@ValueSource(ints = { -1, 0, 100 })
void testValues(int value) {
    // Testing simple pass-through logic
}
```

Prefer focused single test:

```java
@Test
void testValue() {
    // Test with representative value
}
```

For JSON validation, use specialized assertions:

```java
// Instead of string contains checks:
assertThat(entity.getBody()).contains("\"name\":\"test\"");

// Use structured assertions:
JsonContent body = new JsonContent(entity.getBody());
assertThat(body).extractingPath("name").isEqualTo("test");
```

When testing output, prefer CapturedOutput over complex mocks:

```java
@Test
void testOutput(CapturedOutput output) {
    // Trigger output
    assertThat(output).contains("expected message");
}
```

Reserve integration tests for validating system interactions that cannot be effectively tested at the unit level.