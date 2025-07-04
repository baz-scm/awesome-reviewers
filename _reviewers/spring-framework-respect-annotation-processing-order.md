---
title: Respect annotation processing order
description: When designing Spring components, pay careful attention to the order
  in which annotations are processed, especially for inheritance scenarios. Spring
  processes annotations in a specific sequence that can affect bean initialization
  and override behavior.
repository: spring-projects/spring-framework
label: Spring
language: Java
comments_count: 5
repository_stars: 58382
---

When designing Spring components, pay careful attention to the order in which annotations are processed, especially for inheritance scenarios. Spring processes annotations in a specific sequence that can affect bean initialization and override behavior.

1. Ensure interface-level annotations are processed before class-level annotations when appropriate. This ordering allows local annotations to override behavior from inherited interfaces.

```java
// DO: Process interface annotations before local class annotations
for (SourceClass ifc : sourceClass.getInterfaces()) {
    collectImports(ifc, imports, visited);
}
imports.addAll(sourceClass.getAnnotationAttributes(Import.class.getName(), "value"));
```

2. Validate annotation usage at appropriate scope levels. Throw exceptions when annotations are used at an incorrect scope rather than silently ignoring them:

```java
// DO: Validate annotation usage
if (executionPhase == ExecutionPhase.BEFORE_TEST_CLASS && !isClassLevel) {
    throw new IllegalArgumentException("Class-level phase cannot be used on method-level annotation");
}
```

3. When managing bean definitions, be cautious about bean overrides. Redefinitions of beans with the same name but different definitions can lead to unpredictable behavior if allowed silently:

```java
// Consider explicitly handling bean definition conflicts
if (!isAllowBeanDefinitionOverriding() && existingDefinition != null 
        && !existingDefinition.equals(beanDefinition)) {
    throw new BeanDefinitionOverrideException(beanName, beanDefinition, existingDefinition);
}
```

4. When implementing autowiring for components with potential duplicates, prefer clear methods that show the intent rather than relying on Optional parameters:

```java
// Better approach for single-instance configurers
@Autowired(required = false)
void setAsyncConfigurer(AsyncConfigurer asyncConfigurer) {
    if (asyncConfigurer != null) {
        this.executor = asyncConfigurer::getAsyncExecutor;
        this.exceptionHandler = asyncConfigurer::getAsyncUncaughtExceptionHandler;
    }
}
```