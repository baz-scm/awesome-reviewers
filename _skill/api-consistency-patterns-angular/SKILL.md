---
name: api-consistency-patterns-angular
description: "Ensure Angular APIs are designed and refactored for consistency in naming, return types, and usage conventions."
---

# API Consistency Patterns (Angular)

When designing or reviewing Angular APIs, strive for consistency across similar functions and modules[6]. Inconsistent APIs confuse developers and introduce bugs. Key consistency patterns to enforce:

1. **Uniform return types.** If other APIs use a wrapper type (e.g. `OneOrMany<T>`), your API should not arbitrarily return raw types vs arrays. Stick to the established pattern for single vs multiple values[7].
2. **Consistent capabilities.** Similar handlers or services should offer similar capabilities. For example, if animation event handlers in one part of the framework support certain options, handlers elsewhere should support them too[7].
3. **Standardized creation patterns.** Don’t mix factories, constructors, and static methods randomly. Choose one pattern for creating similar objects and use it everywhere (e.g. always use static factory methods instead of sometimes using `new`)[7][8].
4. **Organized exports.** Related APIs should be exported from the same module or package area for discoverability[9].
5. **Behavioral consistency.** Ensure that functions meant to do analogous things don’t have divergent behavior. Equivalent inputs should yield equivalent outcomes across the codebase[9].

For example, in Angular’s codebase a function originally returned either a single error or an array of errors, which was inconsistent. The improved approach was to use `OneOrMany<Error>` uniformly, matching other APIs[10]. By applying these patterns, the API surface remains predictable and easier to learn, reducing developer cognitive load and bugs[11].
