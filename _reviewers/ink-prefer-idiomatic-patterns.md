---
title: prefer idiomatic patterns
description: Choose language-native methods and control structures that make code
  more readable and maintainable. Use built-in functions instead of manual implementations,
  select appropriate control flow structures, and write explicit code that clearly
  communicates intent.
repository: vadimdemedes/ink
label: Code Style
language: JavaScript
comments_count: 4
repository_stars: 31825
---

Choose language-native methods and control structures that make code more readable and maintainable. Use built-in functions instead of manual implementations, select appropriate control flow structures, and write explicit code that clearly communicates intent.

Examples of preferred patterns:
- Use `char.repeat(max)` instead of manual string concatenation loops
- Use switch statements instead of multiple if-else chains when handling discrete values
- Use explicit return statements in cleanup functions: `return () => { cleanup(); };` rather than `return () => cleanup();` when you don't want to return the cleanup function's result
- Use cleaner import paths that leverage package.json configuration

This approach reduces cognitive load, leverages language features effectively, and makes code intentions clearer to other developers.