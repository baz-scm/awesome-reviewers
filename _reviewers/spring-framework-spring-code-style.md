---
title: Spring code style
description: "Follow Spring Framework's code style guidelines to ensure consistency\
  \ across the codebase. Key rules include:\n\n1. **Import statements**: \n   - Use\
  \ specific imports rather than wildcard imports"
repository: spring-projects/spring-framework
label: Code Style
language: Java
comments_count: 13
repository_stars: 58382
---

Follow Spring Framework's code style guidelines to ensure consistency across the codebase. Key rules include:

1. **Import statements**: 
   - Use specific imports rather than wildcard imports
   - Maintain consistent import ordering
   - Avoid static imports except in specific cases

2. **Field and variable references**:
   - Always prefix instance field references with `this.`
   - Don't declare local variables as `final` unless there's a compelling reason
   - Don't use `var` in production code

3. **Formatting**:
   - Use tabs for indentation, not spaces
   - Remove unnecessary spaces inside parentheses
   - Aim for 90 characters per line (maximum 120), with 80 for Javadoc
   - Place opening braces on the same line, `else` statements on a new line

4. **Before submitting**:
   - Run `./gradlew check` to catch style violations automatically

Example of proper style:
```java
public class MyClass {
    private final String field;

    public MyClass(String parameter) {
        this.field = parameter;
    }

    public void doSomething(String input) {
        if (input == null) {
            return;
        }
        else {
            String result = processInput(this.field, input);
            processResult(result);
        }
    }
}
```