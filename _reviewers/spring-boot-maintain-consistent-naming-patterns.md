---
title: Maintain consistent naming patterns
description: 'Follow established naming patterns and conventions throughout the codebase
  to ensure consistency and clarity. This includes:


  1. Use existing naming patterns for similar concepts:'
repository: spring-projects/spring-boot
label: Naming Conventions
language: Java
comments_count: 7
repository_stars: 77637
---

Follow established naming patterns and conventions throughout the codebase to ensure consistency and clarity. This includes:

1. Use existing naming patterns for similar concepts:
   - Follow established suffixes (e.g., *BuilderCustomizer for builder customization interfaces)
   - Maintain consistent method naming patterns across related classes
   - Use consistent property naming schemes (avoid mixing kebab-case and camelCase)

2. Choose clear, descriptive names that avoid jargon:
   ```java
   // Avoid unclear or ambiguous names
   enum SameSite {
     UNSET("Unset")  // Makes readers stop and think
   }
   
   // Use clear, descriptive names
   enum SameSite {
     OMITTED("Omitted")  // Clearly describes the behavior
   }
   ```

3. Write descriptive test method names that explain the test scenario:
   ```java
   // Avoid vague names
   @Test
   void customizer() { }
   
   // Use descriptive names that explain the test
   @Test
   void whenCustomizerBeanIsDefinedThenItIsConfiguredOnSpringLiquibase() { }
   ```

4. Avoid unnecessary renaming that doesn't add value but increases diff complexity and makes code reviews harder.