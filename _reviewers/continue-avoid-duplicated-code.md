---
title: Avoid duplicated code
description: Identify and extract shared functionality between classes into reusable
  components. Code duplication increases maintenance burden and risk of inconsistent
  behavior when changes are needed.
repository: continuedev/continue
label: Code Style
language: Kotlin
comments_count: 2
repository_stars: 27819
---

Identify and extract shared functionality between classes into reusable components. Code duplication increases maintenance burden and risk of inconsistent behavior when changes are needed.

Use these approaches to eliminate duplication:
1. Create abstract base classes for related services
2. Extract common functionality into utility methods
3. Encapsulate data structures with their utility methods in dedicated classes

Example of problematic duplication:
```kotlin
// In NextEditService
fun triggerNextEdit() {
    // Almost identical code to triggerCompletion() in AutocompleteService
    // with minor differences
}

// In AutocompleteService  
fun triggerCompletion() {
    // Almost identical code to triggerNextEdit() in NextEditService
    // with minor differences
}
```

Better approach:
```kotlin
// In a shared abstract base class or utility class
abstract class EditServiceBase {
    protected fun triggerEdit(editType: String, parameters: Map<String, Any>) {
        // Common implementation
    }
}

// In concrete implementations
class NextEditService : EditServiceBase() {
    fun triggerNextEdit() {
        triggerEdit("nextEdit", specificParameters)
    }
}

class AutocompleteService : EditServiceBase() {
    fun triggerCompletion() {
        triggerEdit("completion", specificParameters)
    }
}
```

For data types with associated utilities, follow the pattern demonstrated in `RangeInFileWithContents` where data and its manipulation methods are encapsulated together.