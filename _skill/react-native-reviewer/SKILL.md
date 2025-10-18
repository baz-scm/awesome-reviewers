---
name: react-native-reviewer
description: "Guidelines for reviewing React Native code, emphasizing null-safety and performance optimizations in mobile application development."
license: CC-BY-4.0
---

# React Native Code Review Guidelines

## Null Safety and Clarity
In React Native (especially Android/Kotlin code), avoid using the non-null assertion operator `!!` which can crash the app if the value is unexpectedly null[8]. Instead, use safer alternatives provided by the language: for example, `checkNotNull()` or `requireNotNull()` to explicitly handle null cases with meaningful errors[9], or the Elvis operator `?:` to supply default values or throw exceptions when encountering null[10]. Leveraging Kotlin’s smart casting (`is` checks) and nullable types properly can eliminate the need for `!!` by handling the null case in a safe manner[11]. By ensuring all potentially null values are checked or handled, you prevent runtime crashes and make the code’s assumptions explicit.

## Performance Optimizations
React Native code (both JavaScript and native modules) should minimize unnecessary memory allocations and computations to maintain app performance[12]. Look for opportunities to reuse objects and avoid redundant work. For instance, avoid creating new objects or data copies if not needed: reuse existing data structures or use references to prevent extra garbage collection overhead[13][14]. In C++ modules, prefer polymorphism or references over making duplicate copies of objects; for example, don’t wrap an object in a new `shared_ptr` if you can pass the object directly and leverage polymorphic behavior[13]. Likewise, avoid copying collections when a read-only reference will do (use `const&` in C++ or immutable data in JS)[14]. Employ lazy evaluation for expensive operations, calculating results only when needed instead of precomputing everything upfront[13][14]. These practices reduce memory pressure and CPU usage, leading to smoother, more efficient React Native apps.
