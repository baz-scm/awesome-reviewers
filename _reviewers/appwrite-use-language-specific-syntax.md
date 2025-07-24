---
title: Use language-specific syntax
description: 'Code snippets must use the correct language-specific syntax and include
  all necessary imports to compile properly. When writing examples:


  1. Include all required imports for the libraries and data structures used'
repository: appwrite/appwrite
label: Code Style
language: Markdown
comments_count: 6
repository_stars: 51959
---

Code snippets must use the correct language-specific syntax and include all necessary imports to compile properly. When writing examples:

1. Include all required imports for the libraries and data structures used
2. Use language-appropriate collection initializers and factories
3. Ensure code is placed in the correct language directory
4. Avoid mixing syntax from different languages (e.g., Kotlin syntax in Java files)

**Bad Example (Java file with Kotlin syntax):**
```java
import io.appwrite.services.Databases;

Databases databases = new Databases(client);
databases.updateDocuments(
    "<DATABASE_ID>",
    "<COLLECTION_ID>",
    mapOf("a" to "b"),  // Wrong: Using Kotlin syntax in Java
    listOf()            // Wrong: Using Kotlin syntax in Java
);
```

**Good Example (Java file with Java syntax):**
```java
import io.appwrite.services.Databases;
import java.util.Map;
import java.util.List;

Databases databases = new Databases(client);
databases.updateDocuments(
    "<DATABASE_ID>",
    "<COLLECTION_ID>", 
    Map.of("a", "b"),   // Correct: Using Java Map factory
    List.of()           // Correct: Using Java List factory
);
```

Proper language-specific syntax improves code readability and ensures examples actually compile and run correctly for developers.