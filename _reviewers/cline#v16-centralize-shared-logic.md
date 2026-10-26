---
title: Centralize Shared Logic
description: 'Code should avoid parallel implementations and scattered branching:


  - Reuse existing shared/core helpers instead of duplicating logic in app/feature
  code (e.g., remote normalization, shell-kind detection, session title inference).'
repository: cline/cline#v16
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70882
---

Code should avoid parallel implementations and scattered branching:

- Reuse existing shared/core helpers instead of duplicating logic in app/feature code (e.g., remote normalization, shell-kind detection, session title inference).
- If you need new behavior, extend the existing module/formatter rather than adding a second copy. Centralize shared formatting/escaping rules in one place (e.g., use a discriminated union so one formatter handles tool vs run-start while keeping identical escaping/trimming logic consolidated).
- Replace repeated `if/else` chains for cross-cutting concerns with one-time role/strategy dispatch created at the start (e.g., choose an `outputter` once based on `outputMode`, then call straight-line lifecycle methods; verbosity can be passed into outputters so orthogonal behavior doesn’t create new conditional paths).
- Cleanliness conventions: remove unused imports, avoid magic numbers by using named constants, and document intent for timing/cleanup behavior.

Example (role-based outputter pattern):
```ts
export async function runAgent(config: { outputMode: 'json'|'console'; verbose: boolean }) {
  const outputter = config.outputMode === 'json'
    ? new JsonRunOutputter({ verbose: config.verbose })
    : new ConsoleRunOutputter({ verbose: config.verbose });

  outputter.runStarted();
  try {
    const result = await doWork();
    outputter.runResult(result);
  } catch (e) {
    outputter.runAborted(e);
    throw e;
  }
}
```

Example (no duplication: one formatter via union):
```ts
type HookOrigin =
  | { kind: 'tool'; toolName: string; toolCallId: string }
  | { kind: 'runStart' };

function formatHookContextBlock(origin: HookOrigin, text: string): string {
  const body = text.trim().replace(/<(\/?)hook_context/gi, '<\\$1hook_context');
  if (origin.kind === 'tool') {
    return `<hook_context source="${origin.kind==='tool' ? 'Tool' : ''}" tool_name="${origin.toolName}" tool_call_id="${origin.toolCallId}">\n${body}\n</hook_context>`;
  }
  return `<hook_context source="RunStart">\n${body}\n</hook_context>`;
}
```

Applying these consistently makes code easier to read, reduces bugs from divergent behavior, and improves long-term maintainability.