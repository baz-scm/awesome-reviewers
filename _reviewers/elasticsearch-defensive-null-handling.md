---
title: Defensive null handling
description: 'Always handle null references and values defensively to prevent NullPointerExceptions
  and unexpected behavior. Follow these practices:


  1. **Check nulls before dereferencing**: Always verify a reference is not null before
  accessing its methods or properties:'
repository: elastic/elasticsearch
label: Null Handling
language: Java
comments_count: 4
repository_stars: 73104
---

Always handle null references and values defensively to prevent NullPointerExceptions and unexpected behavior. Follow these practices:

1. **Check nulls before dereferencing**: Always verify a reference is not null before accessing its methods or properties:
```java
// Instead of directly accessing possibly null objects
Engine engine = shard.getEngineOrNull();
assertThat(engine != null && engine.isThrottled(), equalTo(true));

// Or for parsing operations
if (token == null) {
    token = parser.nextToken();
}
```

2. **Use APIs that handle nulls gracefully**: Prefer methods that allow specifying default values when parsing or converting:
```java
// Instead of Boolean.parseBoolean which doesn't handle nulls well
assertThat(Booleans.parseBoolean((String) indexSettings.get(setting.getKey()), false), matcher);
```

3. **Defensive coding for asynchronous operations**: When objects might be deleted or changed by other threads:
```java
var project = clusterService.state().metadata().projects().get(projectId);
PersistentTasksCustomMetadata.PersistentTask<?> persistentTask = 
    project == null ? null : PersistentTasksCustomMetadata.getTaskWithId(project, getPersistentTask());
```

These patterns help create more robust code that can handle edge cases and prevent crashes in production.
