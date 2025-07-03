---
title: Design extensible stable APIs
description: When designing public APIs, prioritize extensibility while maintaining
  backward compatibility and implementation hiding. This ensures APIs can evolve without
  breaking existing clients while allowing for future enhancements.
repository: JetBrains/kotlin
label: API
language: Kotlin
comments_count: 7
repository_stars: 50857
---

When designing public APIs, prioritize extensibility while maintaining backward compatibility and implementation hiding. This ensures APIs can evolve without breaking existing clients while allowing for future enhancements.

Key principles:
1. Never change visibility levels of public API elements
2. Use flexible extension mechanisms instead of fixed enums
3. Keep implementation details in separate packages
4. Design clear extension points for third-party implementations

Example:
```kotlin
// Instead of enum-based priority
enum class Priority { LOW, NORMAL, HIGH } // Difficult to extend

// Use comparable class
class Priority(val value: Int) : Comparable<Priority> {
    companion object {
        val LOW = Priority(0)
        val NORMAL = Priority(1000)
        val HIGH = Priority(2000)
    }
    
    override fun compareTo(other: Priority): Int = 
        value.compareTo(other.value)
}

// This allows third parties to insert custom priorities
val CUSTOM = Priority(1500) // Between NORMAL and HIGH
```

This approach:
- Maintains consistent visibility across all API surfaces
- Allows for future extensibility without breaking changes 
- Clearly separates public API from implementation details
- Enables third-party extensions through well-defined mechanisms
