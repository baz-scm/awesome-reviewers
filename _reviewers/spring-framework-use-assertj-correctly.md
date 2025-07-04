---
title: Use AssertJ correctly
description: 'Spring Framework tests must use AssertJ for assertions rather than JUnit''s
  `Assertions`, Spring''s `Assert` class, or plain `assert` statements. Follow these
  AssertJ best practices:'
repository: spring-projects/spring-framework
label: Testing
language: Java
comments_count: 7
repository_stars: 58382
---

Spring Framework tests must use AssertJ for assertions rather than JUnit's `Assertions`, Spring's `Assert` class, or plain `assert` statements. Follow these AssertJ best practices:

1. Use fluent assertions with proper methods:
   ```java
   // PREFERRED
   assertThat(collection).hasSize(2);
   
   // AVOID
   assertThat(collection.size()).isEqualTo(2);
   ```

2. For exception testing, use:
   ```java
   // PREFERRED
   assertThatExceptionOfType(BadSqlGrammarException.class).isThrownBy(() -> {
       jdbcTemplate.queryForList("SELECT name FROM user", String.class);
   });
   
   // AVOID
   try {
       jdbcTemplate.queryForList("SELECT name FROM user", String.class);
       fail("BadSqlGrammarException should have been thrown");
   }
   catch (BadSqlGrammarException expected) {
   }
   ```

3. For code that shouldn't throw exceptions:
   ```java
   // PREFERRED
   assertThatCode(() -> {
       Assert.noNullElements(asList("foo", "bar"), "enigma");
   }).doesNotThrowAnyException();
   
   // AVOID
   Assert.noNullElements(asList("foo", "bar"), "enigma"); // Missing verification
   ```

Using AssertJ consistently provides more readable tests, better failure messages, and ensures test consistency throughout the codebase.