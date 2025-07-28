---
title: Semantic identifier naming patterns
description: 'Use consistent naming patterns that reflect the semantic role of identifiers:


  1. Constants should use UPPER_SNAKE_CASE:

  ```

  const MAX_RETRY_COUNT = 3;'
repository: helix-editor/helix
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 39026
---

Use consistent naming patterns that reflect the semantic role of identifiers:

1. Constants should use UPPER_SNAKE_CASE:
```
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = "https://api.example.com";
```

2. Type names should use TitleCase:
```
struct UserProfile { }
class DatabaseConnection { }
```

3. Functions/methods should use camelCase:
```
fn calculateTotal() { }
fn validateUserInput() { }
```

4. Member variables should use a consistent prefix (e.g., m_) to clearly identify class/struct members:
```
struct Widget {
    m_width: i32,
    m_height: i32
}
```

This pattern makes code more readable by allowing quick visual identification of an identifier's role. It also helps catch semantic errors where identifiers might be used incorrectly (e.g., using a type name where a function was intended).