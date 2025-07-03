---
title: Name reflects meaning
description: 'Choose names that clearly communicate the intent, behavior, and semantics
  of code elements. Names should be accurate, consistent, and follow established patterns:'
repository: elastic/elasticsearch
label: Naming Conventions
language: Java
comments_count: 9
repository_stars: 73104
---

Choose names that clearly communicate the intent, behavior, and semantics of code elements. Names should be accurate, consistent, and follow established patterns:

1. **Method names must reflect what they operate on**: If a method manipulates indices, name it accordingly (e.g., `moveIndicesToPreviouslyFailedStep` rather than `moveClusterStateToPreviouslyFailedStep`). Method names should express what they do, not how they do it.

2. **Variable names should precisely describe their content**: Use terms that clearly convey meaning, especially for metrics or measurements:
   ```java
   // Unclear - doesn't specify these are averages
   int percentWriteThreadPoolUtilization;
   long maxTaskTimeInWriteQueueMillis;
   
   // Clear - precisely describes the metrics
   int averageWriteThreadPoolUtilization;
   long averageWriteThreadPoolQueueLatency;
   ```

3. **Use consistent naming patterns**: Follow established patterns within the codebase and respect external conventions:
   - For third-party products, match their official capitalization (e.g., "IBM watsonx" not "IBM WatsonX")
   - For test methods, follow JUnit conventions (begin with "test" using camelCase)
   - For task queues, ensure names match their purpose (e.g., "update-data-stream-mappings" for mappings-related tasks)

4. **Prefer constants over string literals**: Extract repeated or semantically meaningful strings into named constants:
   ```java
   // Hard to maintain - string literals scattered throughout code
   if (configs.group.equals("unsupported") || configs.group.equals("union-types")) {
   
   // Better - using named constants
   private static final String GROUP_UNSUPPORTED = "unsupported";
   private static final String GROUP_UNION_TYPES = "union-types";
   
   if (configs.group.equals(GROUP_UNSUPPORTED) || configs.group.equals(GROUP_UNION_TYPES)) {
   ```
