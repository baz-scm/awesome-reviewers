---
title: Documentation style consistency
description: 'Maintain consistent documentation style to improve readability and user
  experience:


  1. **Use precise terminology**: When referencing features or components, use their
  full and correct names.'
repository: quarkusio/quarkus
label: Documentation
language: Other
comments_count: 4
repository_stars: 14667
---

Maintain consistent documentation style to improve readability and user experience:

1. **Use precise terminology**: When referencing features or components, use their full and correct names.
   ```
   # Better
   The Apicurio Dev Services supports xref:compose-dev-services.adoc[Compose Dev Services].
   
   # Avoid
   The Apicurio Dev Services supports xref:compose-dev-services.adoc[Compose].
   ```

2. **Address readers directly**: Use "you" instead of "users" or other third-person references in documentation.
   ```
   # Better
   You must configure the annotation processor in your build tool:
   
   # Avoid
   Users are required to make an extra step of configuring the annotation processor...
   ```

3. **Maintain consistent terminology**: Choose one term for a concept and use it consistently throughout documentation. If multiple terms exist (e.g., Jakarta Validation vs. Hibernate Validator), explain the relationship once and then use a single term consistently.

4. **Follow established capitalization conventions**: Use lowercase for common terms unless they're proper names or at the beginning of sentences.
   ```
   # Better
   ...automatically provides an RSA-256 key pair for you in dev mode.
   
   # Avoid
   ...automatically provides an RSA-256 key pair for you in Dev Mode.
   ```

When writing or updating documentation, ensure your content aligns with these style guidelines to maintain consistency across the project's documentation.