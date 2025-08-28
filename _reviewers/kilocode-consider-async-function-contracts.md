---
title: Consider async function contracts
description: Be intentional when marking functions as async, as it changes the function's
  contract and caller expectations. Avoid using async unnecessarily when you're just
  returning a promise explicitly, and consider whether making a function async implies
  that callers should await its completion.
repository: kilo-org/kilocode
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 7302
---

Be intentional when marking functions as async, as it changes the function's contract and caller expectations. Avoid using async unnecessarily when you're just returning a promise explicitly, and consider whether making a function async implies that callers should await its completion.

For example, avoid this pattern where async adds no value:
```typescript
// Unnecessary async - just returning a promise
private static async requestLLMFix(code: string, error: string): Promise<string | null> {
    return somePromiseReturningFunction(code, error)
}
```

Also consider the broader implications when converting functions to async:
```typescript
// Before: synchronous activation
export function activate(context: vscode.ExtensionContext) {
    // setup code
    Promise.resolve(vscode.commands.executeCommand("command"))
}

// After: now returns Promise, implying callers should await
export async function activate(context: vscode.ExtensionContext) {
    // setup code  
    await vscode.commands.executeCommand("command")
}
```

The async version changes the contract - callers now expect to await the activation, which may not be the intended behavior for lifecycle functions.