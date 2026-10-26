---
title: Centralize Variability Handling
description: When code behavior varies by “mode/state” (output format, run phase,
  platform shell type, plugin callback capability), avoid scattering conditional branches
  and duplicated helpers. Centralize the variation behind explicit abstractions and
  shared utilities.
repository: cline/cline#v24
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70891
---

When code behavior varies by “mode/state” (output format, run phase, platform shell type, plugin callback capability), avoid scattering conditional branches and duplicated helpers. Centralize the variation behind explicit abstractions and shared utilities.

**Standards**
1. **Encapsulate variability behind roles**: Replace repeated `if (mode === ...)` branches with a single factory/strategy object created once per operation.
2. **Generalize duplicate logic with discriminated unions**: If two functions do the same trimming/escaping/wrapping with small differences, unify them into one formatter/adapter that selects behavior based on a tagged union.
3. **Reuse shared utilities**: Prefer importing canonical helpers from shared packages over re-implementing platform checks or inference logic locally.
4. **Model state with unions, not booleans**: When there are multiple meaningful states, use a string/enum union (discriminated) to prevent invalid combinations and improve testability.
5. **Preserve callback receiver/context**: When wrapping plugin-provided functions, call them with the intended receiver so `this`-dependent code keeps working.

**Example patterns**
- Role/strategy for mode-specific output:
```ts
interface RunOutputter {
  runStarted(...args: unknown[]): void;
  runResult(...args: unknown[]): void;
  runAborted(...args: unknown[]): void;
}

function createRunOutputter(outputMode: string, verbose: boolean): RunOutputter {
  return outputMode === "json"
    ? new JsonRunOutputter({ verbose })
    : new ConsoleRunOutputter({ verbose });
}
```
- Generalized formatter using a tagged union:
```ts
type HookContextInput =
  | { kind: "tool"; toolName: string; toolCallId: string; text: string }
  | { kind: "runStart"; text: string };

function formatHookContext(input: HookContextInput): string {
  const body = input.text.trim().replace(/<(\/?)hook_context/gi, "<\\$1hook_context");
  return input.kind === "tool"
    ? `<hook_context source="Tool" tool_name="${input.toolName}" tool_call_id="${input.toolCallId}">\n${body}\n</hook_context>`
    : `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```
- Preserve receiver when invoking callbacks:
```ts
// If plugin supplies rule.content that relies on `this`, preserve it.
return content.call(rule);
```

Applying these consistently reduces complexity, duplication, and subtle correctness regressions while making code paths easier to read and test.