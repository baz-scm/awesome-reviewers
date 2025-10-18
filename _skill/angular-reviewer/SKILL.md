---
name: angular-reviewer
description: "Guidelines for reviewing Angular framework code, focusing on clear naming and consistent API design across the codebase."
license: CC-BY-4.0
---

# Angular Code Review Guidelines

## Descriptive Naming
Angular code should use clear, self-documenting names for variables, functions, and types[15]. Avoid generic or overly terse names that obscure intent. For example, prefer a constant like `MAX_ANIMATION_DURATION` over a vague `ANIMATION_TIMEOUT`[16], and a type alias like `IgnoreUnknownProps<T>` instead of something like `DeepStripStringIndexUnknown<T>`[16]. Method names should reflect their behavior; e.g., `trackClasses()` is more descriptive than `addClasses()` when the method is actually tracking changes rather than simply adding DOM classes[17]. A good rule is to choose “the shortest name that unambiguously and meaningfully describes” the entity’s purpose[18]. By adopting descriptive naming, the code becomes easier to understand and maintain, as each identifier immediately conveys its role.

## API Consistency
Ensure that similar APIs in Angular follow consistent patterns and conventions[19]. When reviewing new public APIs or changes, check that they align with existing conventions in Angular’s framework. Key aspects include: return types – use established helper types or patterns (e.g. Angular might use `OneOrMany<T>` to allow single or array values) consistently across the codebase[20][21]; method capabilities – if two services or components have similar functionality, their APIs should offer parallel “shape” and expressiveness so that developers have a uniform experience[20][21]; usage patterns – creation and initialization of similar constructs should be done the same way everywhere (for example, always using factory methods versus sometimes constructors)[22][23]. Also ensure consistent import and export locations for related features (keep public API surface well-organized). By maintaining consistency in API design and terminology, Angular developers can rely on familiar patterns, reducing learning curve and preventing errors from confusion[24].
