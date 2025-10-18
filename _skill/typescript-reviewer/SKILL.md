---
name: typescript-reviewer
description: "Guidelines for reviewing Microsoft TypeScript compiler code, focusing on algorithmic efficiency and developer-friendly error messaging."
license: CC-BY-4.0
---

# TypeScript Compiler Code Review Guidelines

## Algorithmic Efficiency
The TypeScript compiler deals with complex algorithms (type checking, program analysis), so it’s crucial to optimize critical loops and recursive operations[46]. When reviewing code that iterates over large sets (files, AST nodes, types) or has nested loops, check that it is as efficient as possible. For instance, avoid naive nested loops that lead to quadratic behavior when a single-pass algorithm would suffice[47][48]. An example from a path normalization routine shows that repeatedly using string operations in a loop was refactored into one linear traversal of the string, which improved performance by avoiding repeated searches[47][48]. Look for opportunities for early exits in loops (break out once you’ve found what you need) and for structuring data to match the access patterns (e.g., using maps or sets for fast lookups instead of scanning arrays)[49]. Also apply tail recursion optimization or an explicit stack for deeply recursive algorithms to prevent potential stack overflow. In summary, ensure any critical section of code has been analyzed for complexity and uses optimal structures and patterns to handle the workload.

## Actionable Error Messages
Error messages in the compiler (and related tooling) should not only indicate what went wrong, but also guide the developer on how to fix the issue[50]. When reviewing changes to TypeScript’s error reporting, make sure messages include specific and helpful details. This means referencing the exact code element that caused the error and, when possible, suggesting a resolution or next step[51]. For example, if a certain syntax is not allowed under a configuration, the error message could advise how to change the config or code to resolve the error[52]. A real instance: instead of a generic error like “Imports/exports cannot be used here,” TypeScript now provides a message that explains you’re in a CommonJS file and suggests adjusting the `type` field in `package.json` or changing compiler settings[53]. Such detail dramatically improves the developer experience by reducing guesswork. As a reviewer, ensure new errors or warnings follow this practice: they should be clear, specific, and whenever feasible, offer a hint or solution path. This helps developers using TypeScript to quickly address issues without frustration[54].
