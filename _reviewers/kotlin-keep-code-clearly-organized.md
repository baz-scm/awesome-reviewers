---
title: Keep code clearly organized
description: Maintain code readability and organization by extracting focused, well-named
  functions and using appropriate scoping. Break down complex logic into smaller,
  focused functions and utilize extension functions when appropriate to improve code
  clarity.
repository: JetBrains/kotlin
label: Code Style
language: Kotlin
comments_count: 7
repository_stars: 50857
---

Maintain code readability and organization by extracting focused, well-named functions and using appropriate scoping. Break down complex logic into smaller, focused functions and utilize extension functions when appropriate to improve code clarity.

Key guidelines:
- Extract complex or repeated logic into separate functions
- Use extension functions for operations that logically belong to a type
- Keep function responsibilities focused and single-purpose
- Place related code together for better context

Example - Before:
```kotlin
fun isValidFloat(s: String): Boolean {
    var start = 0
    var end = s.length - 1
    while (start <= end && s[start].code <= 0x20) start++
    if (start > end) return false
    while (end > start && s[end].code <= 0x20) end--
    if (s[start] == '+' || s[start] == '-') start++
    if (start > end) return false
    // ... more complex logic
}
```

After:
```kotlin
fun isValidFloat(s: String): Boolean {
    val (start, end) = s.findContentBounds() ?: return false
    val (newStart, hasSign) = s.parseSign(start) 
    if (newStart > end) return false
    // ... more focused logic
}

private fun String.findContentBounds(): Pair<Int, Int>? {
    var start = 0
    var end = length - 1
    while (start <= end && this[start].code <= 0x20) start++
    if (start > end) return null
    while (end > start && this[end].code <= 0x20) end--
    return start to end
}

private fun String.parseSign(start: Int): Pair<Int, Boolean> {
    return when (this[start]) {
        '+', '-' -> (start + 1) to true
        else -> start to false
    }
}
```
