---
title: Prefer role and union
description: 'When adding behavior, reduce duplication and conditional sprawl by modeling
  variants explicitly and centralizing shared logic.


  **Standards**

  - **Use roles/interfaces for output/handlers**: Create an outputter once (e.g.,
  `JsonRunOutputter` vs `ConsoleRunOutputter`) and call straight-line lifecycle methods,
  instead of repeatedly branching `if (outputMode...'
repository: cline/CLINE
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70839
---

When adding behavior, reduce duplication and conditional sprawl by modeling variants explicitly and centralizing shared logic.

**Standards**
- **Use roles/interfaces for output/handlers**: Create an outputter once (e.g., `JsonRunOutputter` vs `ConsoleRunOutputter`) and call straight-line lifecycle methods, instead of repeatedly branching `if (outputMode === 'json')` throughout the run path.
- **Use discriminated unions (or string unions) for state/variants**: Avoid booleans when multiple meaningful states exist; prefer unions like `resumed?: 'yes' | 'no'` (or `agent_start`/`agent_resume`) and discriminated unions for formatter variants.
- **Centralize shared formatting/escaping**: If two code paths do the same trimming + tag escaping + wrapper construction, consolidate it into one formatter that switches only on the variant.
- **Don’t reintroduce existing helpers**: If a shared/core utility already provides the behavior (e.g., shell detection), reuse it rather than adding a parallel function.
- **Keep modules focused**: If a PR introduces lots of tool-specific behavior, move it to a dedicated tool/domain module instead of bloating a general-purpose file.

**Example (centralized formatter with discriminated union)**
```ts
type HookContextVariant =
  | { kind: 'tool'; toolName: string; toolCallId: string }
  | { kind: 'runStart'; source: 'RunStart' };

function escapeEmbeddedHookContexts(text: string) {
  return text.trim().replace(/<(\/?)hook_context/gi, '<\\$1hook_context');
}

function formatHookContextBlock(body: string, v: HookContextVariant): string {
  const escaped = escapeEmbeddedHookContexts(body);

  if (v.kind === 'tool') {
    return `<hook_context source="${v.toolName}" tool_name="${v.toolName}" tool_call_id="${v.toolCallId}">\n${escaped}\n</hook_context>`;
  }

  return `<hook_context source="${v.source}">\n${escaped}\n</hook_context>`;
}
```
Apply the same principle to run/output handling: choose the correct implementation once, then use consistent method names and straight-line lifecycle calls.