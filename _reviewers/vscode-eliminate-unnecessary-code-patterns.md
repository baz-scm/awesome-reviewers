---
title: Eliminate unnecessary code patterns
description: 'Remove redundant code patterns that add complexity without value. This
  includes:


  1. Duplicate code blocks - Extract shared logic into reusable functions'
repository: microsoft/vscode
label: Code Style
language: TypeScript
comments_count: 9
repository_stars: 174887
---

Remove redundant code patterns that add complexity without value. This includes:

1. Duplicate code blocks - Extract shared logic into reusable functions
2. Redundant conditions - Avoid rechecking conditions that were already verified
3. Unnecessary control flow - Remove else blocks when if blocks return
4. Repeated inline code - Create helper functions for common patterns

Example of simplifying control flow:

```typescript
// Before
if (filename.endsWith(PROMPT_FILE_EXTENSION)) {
    return filename.slice(0, -PROMPT_FILE_EXTENSION.length);
} else if (filename.endsWith(INSTRUCTION_FILE_EXTENSION)) {
    return filename.slice(0, -INSTRUCTION_FILE_EXTENSION.length);
} else if (filename === COPILOT_CUSTOM_INSTRUCTIONS_FILENAME) {
    return filename.slice(0, -3);
}

// After
if (filename.endsWith(PROMPT_FILE_EXTENSION)) {
    return filename.slice(0, -PROMPT_FILE_EXTENSION.length);
}

if (filename.endsWith(INSTRUCTION_FILE_EXTENSION)) {
    return filename.slice(0, -INSTRUCTION_FILE_EXTENSION.length);
}

if (filename === COPILOT_CUSTOM_INSTRUCTIONS_FILENAME) {
    return filename.slice(0, -3);
}
```

For repeated patterns, extract into helper functions:

```typescript
// Before
const FAILED_TASK_STATUS = { icon: { ...Codicon.error, color: { id: problemsErrorIconForeground } }};
const WARNING_TASK_STATUS = { icon: { ...Codicon.warning, color: { id: problemsWarningIconForeground } }};

// After
const createColoredIcon = (icon: Codicon, colorId: string) => ({ ...icon, color: { id: colorId }});
const FAILED_TASK_STATUS = { icon: createColoredIcon(Codicon.error, problemsErrorIconForeground) };
const WARNING_TASK_STATUS = { icon: createColoredIcon(Codicon.warning, problemsWarningIconForeground) };
```