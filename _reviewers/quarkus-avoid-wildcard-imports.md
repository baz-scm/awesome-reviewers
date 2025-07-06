---
title: Avoid wildcard imports
description: Wildcard (star) imports like `import java.util.*;` are prohibited in
  the codebase as they reduce code readability and can cause naming conflicts. Always
  import specific classes individually.
repository: quarkusio/quarkus
label: Code Style
language: Java
comments_count: 4
repository_stars: 14667
---

Wildcard (star) imports like `import java.util.*;` are prohibited in the codebase as they reduce code readability and can cause naming conflicts. Always import specific classes individually.

Configure your IDE to disallow wildcard imports:
- In IntelliJ IDEA: Navigate to Editor -> Code Style -> Java -> Imports and set 'Class count to use import with *' to 999.
- The same setting should be applied for 'Names count to use static import with *'.

Instead of:
```java
import java.util.*;
```

Use:
```java
import java.util.List;
import java.util.Map;
import java.util.Set;
```

This makes dependencies explicit and avoids potential name conflicts when classes with the same name exist in different packages.