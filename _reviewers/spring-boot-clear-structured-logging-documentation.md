---
title: Clear structured logging documentation
description: Document structured logging implementations with clarity, explicitly
  noting precedence rules and interactions with other logging configurations. Always
  highlight important considerations (such as custom configurations taking precedence)
  prominently in the main documentation rather than as footnotes or warnings that
  might be missed.
repository: spring-projects/spring-boot
label: Logging
language: Other
comments_count: 2
repository_stars: 77637
---

Document structured logging implementations with clarity, explicitly noting precedence rules and interactions with other logging configurations. Always highlight important considerations (such as custom configurations taking precedence) prominently in the main documentation rather than as footnotes or warnings that might be missed.

When providing configuration examples:
1. Keep examples as simple as possible for the common case
2. Avoid unnecessary conditional logic unless required for specific scenarios
3. For complex configurations, reference default implementations or provide links to more detailed documentation

Example of good structured logging documentation:

```
# Structured Logging

To enable structured logging, set the property `logging.structured.format.console` (for console output) 
or `logging.structured.format.file` (for file output) to the format ID you want to use.

IMPORTANT: Custom log configurations take precedence over these settings. If you're using custom log 
configuration, you must manually configure structured logging as shown below:

## Basic Implementation
```xml
<encoder class="org.springframework.boot.logging.logback.StructuredLogEncoder">
    <format>${CONSOLE_LOG_STRUCTURED_FORMAT}</format>
    <charset>${CONSOLE_LOG_CHARSET}</charset>
</encoder>
```

For advanced configurations with conditionals, see our [default configurations](link-to-examples).
```

This approach ensures that developers have clear guidance for common cases while maintaining access to more complex options when needed.