---
name: vite-reviewer
description: "Guidelines for reviewing Vite build tool code, focusing on proper TypeScript null handling and clear, precise documentation practices."
license: CC-BY-4.0
---

# Vite Code Review Guidelines

## Idiomatic Null Handling
When reviewing Vite’s TypeScript code, ensure that it handles optional or absent values using idiomatic patterns. Prefer optional properties and types over using null to represent “not yet available” states[62]. For instance, instead of initializing a boolean field to `null` to indicate it will be set later, use an optional (`?`) property which can be `undefined` until assigned[63]. This communicates intent more clearly and leverages TypeScript’s type system. At runtime, encourage using nullish coalescing and optional chaining for clarity. For example, when merging configuration or options, use `??` to supply default objects and `?.` to safely access nested properties[64][65]. Vite’s code should avoid older patterns like checking `typeof x !== 'undefined'` or manual truthiness checks for null; the modern operators make the code cleaner and less error-prone. By consistently using these optional patterns, the codebase remains more readable and aligned with modern JavaScript standards[65].

## Precise Documentation
Vite’s documentation and comments should be written with precision and clarity. Review any doc changes or comments to ensure they use specific language and correct terminology[66]. Avoid vague descriptors—if a comment says “old version,” it should instead specify the exact version (“Vite 5 (old version)”) to remove ambiguity[67]. Encourage the use of proper semantic markup in documentation (for example, using `<strong>` instead of `<b>` for important text in HTML docs) to improve accessibility and meaning[68]. When describing features or limitations, be explicit about their scope. For instance, if a configuration option has limitations, the docs should clearly state what environment or version those limitations apply to, rather than using generalized language[68]. It’s also important to balance detail with maintainability: being precise doesn’t mean overloading with future specifics (like hard-coding upcoming version numbers that might change). The goal is to make documentation accurate and easy to follow[69]. As a reviewer, ensure that every explanation in Vite’s docs clearly defines concepts and instructions so users can understand them without guesswork.
