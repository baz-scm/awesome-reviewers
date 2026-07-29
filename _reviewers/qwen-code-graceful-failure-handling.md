---
title: Graceful Failure Handling
description: 'When an action depends on daemon capabilities or other availability
  checks, never fail silently or hard-fail the whole UI. Instead: (1) gate capability-dependent
  parameters/requests so missing capabilities degrade gracefully, and (2) treat dependency
  outcomes as real failures—don’t return “handled/success” if the operation wasn’t
  actually performed; surface...'
repository: QwenLM/qwen-code
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 26407
---

When an action depends on daemon capabilities or other availability checks, never fail silently or hard-fail the whole UI. Instead: (1) gate capability-dependent parameters/requests so missing capabilities degrade gracefully, and (2) treat dependency outcomes as real failures—don’t return “handled/success” if the operation wasn’t actually performed; surface a user-visible toast/message.

Practical rules:
- Capability gating: Only pass parameters (e.g., `sourceType`) that trigger `requireCapability(...)` if the capability is present; otherwise omit the parameter or use a fallback query.
- No false success: If a helper returns `boolean`/status (e.g., `createSideTask()`), check it. On `false`/unavailable, return a failure indicator consistent with the command flow and notify the user.
- Keep failure paths actionable: provide a warning/error toast and avoid throwing the entire request when a less-fancy mode is acceptable.

Example (combined pattern):
```ts
if (directive.toLowerCase() === 'sider') {
  const ok = createSideTask();
  if (!ok) pushToast('warning', t('sideTask.unavailable'));
  return true;
}

const listOpts: any = { /* ... */ };
if (hasCapability('session_source_metadata')) {
  listOpts.sourceType = WEB_SHELL_SESSION_SOURCE_TYPE;
}
// If capability is missing, omit sourceType to prevent request-wide failure.
```