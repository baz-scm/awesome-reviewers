---
title: Complete API documentation
description: 'Documentation should be complete, accurate, and follow Spring Framework
  conventions. Ensure your Javadocs include:


  1. **Clear and accurate descriptions** that precisely explain behavior and purpose'
repository: spring-projects/spring-framework
label: Documentation
language: Java
comments_count: 10
repository_stars: 58382
---

Documentation should be complete, accurate, and follow Spring Framework conventions. Ensure your Javadocs include:

1. **Clear and accurate descriptions** that precisely explain behavior and purpose
   ```java
   /**
    * Returns a concise description of this {@code HandlerMethod}, which is used
    * in log and error messages.
    * <p>The description should typically include the method signature of the
    * underlying handler method for clarity and debugging purposes.
    */
   ```

2. **Complete parameter documentation** for all parameters, especially in interfaces
   ```java
   /**
    * Called before every retry attempt.
    * @param retryExecution the current retry execution context
    */
   default void beforeRetry(RetryExecution retryExecution) {
   ```

3. **Class-level Javadoc** for all public classes and interfaces

4. **Format standards**: 
   - Wrap Javadoc around 90 characters
   - Don't end `@param` or `@return` descriptions with periods unless they contain sentences
   - Include `@since` tags for all new public methods

5. **Contextual information** about when and how to use the API:
   ```java
   /**
    * Create a builder with the method, URI, headers, cookies, attributes, and body of the given request.
    * @param other the request to copy the method, URI, headers, cookies, attributes, and body from
    * @return the created builder
    * @since 5.3
    */
   ```

6. **Clear behavioral documentation** for methods with special handling:
   ```java
   /**
    * Create a builder with the given method and given string base URI template.
    * <p>The given URI template may contain URI variable placeholders that can be expanded using
    * the methods of the built request.
    * @param method the HTTP method (GET, POST, etc)
    * @param uri the URI template
    * @return the created builder
    * @since 5.3
    */
   ```

Documentation should be specific to the code at hand rather than copied from similar classes, and should clarify edge cases and expected behaviors.