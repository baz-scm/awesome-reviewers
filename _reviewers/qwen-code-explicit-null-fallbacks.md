---
title: Explicit null fallbacks
description: 'When handling `null`/`undefined`, be explicit about intent:

  - **Choose the correct fallback source**: if a variable is `undefined`, ensure `??`
  falls back to the intended “truth” (not a stale previous value). '
repository: QwenLM/qwen-code
label: Null Handling
language: TSX
comments_count: 4
repository_stars: 26407
---

When handling `null`/`undefined`, be explicit about intent:
- **Choose the correct fallback source**: if a variable is `undefined`, ensure `??` falls back to the intended “truth” (not a stale previous value). 
- **Avoid silent dropping**: don’t filter out non-null `ReactNode` variants in a way that changes semantics between render modes (inline vs overflow). If separators/text are part of the host contract, preserve them intentionally.
- **Prefer exhaustiveness over implicit `null`**: for union/enum switches, use an exhaustive pattern so new members don’t silently fall through to `null`.
- **Match tests to the real nullability contract**: if a value is always a boolean, assert `false` (not `undefined`).

Example (routing fallback):
```ts
const reportedWorkspaceCwd = connection.sessionId
  ? connection.workspaceCwd
  : (selectedWorkspaceCwd ?? primaryWorkspaceCwd);
// If selectedWorkspaceCwd is undefined, fall back to primaryWorkspaceCwd—not a stale connection.workspaceCwd.
```

Example (exhaustive switch):
```ts
switch (checks) {
  case 'passing': return ...;
  case 'failing': return ...;
  case 'none': return null;
  default: {
    const _exhaustive: never = checks;
    return null;
  }
}
```

Example (test nullability):
```ts
expect(latestChatEditorProps.disabled).toBe(false); // not undefined
```