---
title: Comprehensive JSDoc with examples
description: 'Write thorough JSDoc comments for interfaces, functions, and methods
  that clearly explain their purpose and behavior. Include:


  1. A main description explaining the component''s purpose'
repository: microsoft/vscode
label: Documentation
language: TypeScript
comments_count: 3
repository_stars: 174887
---

Write thorough JSDoc comments for interfaces, functions, and methods that clearly explain their purpose and behavior. Include:

1. A main description explaining the component's purpose
2. Documentation for all parameters and properties, especially highlighting differences between similarly named items
3. Concrete examples for complex logic to illustrate different use cases

For interfaces:
```typescript
/**
 * Represents a configured task in the system.
 * 
 * This interface is used to define tasks that can be executed within the workspace.
 * It includes optional properties for identifying and describing the task.
 * 
 * Properties:
 * - `type`: (optional) The type of the task, which categorizes it (e.g., "build", "test").
 * - `label`: (optional) A user-facing label for the task, typically used for display purposes.
 * - `_label`: (optional) An internal label for the task, used for unique identification.
 */
interface IConfiguredTask {
    type?: string;
    label?: string;
    _label?: string;
}
```

For functions:
```typescript
/**
 * Determines the type of token based on command line and cursor position.
 * 
 * Examples:
 * - `getTokenType({commandLine: "git commit", cursorPosition: 3}, TerminalShellType.Bash)`
 *   Returns TokenType.Command as cursor is within the command
 * - `getTokenType({commandLine: "git commit -m", cursorPosition: 11}, TerminalShellType.Bash)`
 *   Returns TokenType.Argument as cursor is after a command argument flag
 * 
 * @param ctx The command context containing command line and cursor position
 * @param shellType The type of shell being used
 * @returns The determined token type based on context
 */
function getTokenType(ctx: { commandLine: string; cursorPosition: number }, shellType: TerminalShellType | undefined): TokenType {
    // Implementation
}
```

Prefer descriptive main comments over tag-only documentation and ensure every component of your API is properly documented. This practice significantly improves code maintainability and reduces onboarding time for new developers.