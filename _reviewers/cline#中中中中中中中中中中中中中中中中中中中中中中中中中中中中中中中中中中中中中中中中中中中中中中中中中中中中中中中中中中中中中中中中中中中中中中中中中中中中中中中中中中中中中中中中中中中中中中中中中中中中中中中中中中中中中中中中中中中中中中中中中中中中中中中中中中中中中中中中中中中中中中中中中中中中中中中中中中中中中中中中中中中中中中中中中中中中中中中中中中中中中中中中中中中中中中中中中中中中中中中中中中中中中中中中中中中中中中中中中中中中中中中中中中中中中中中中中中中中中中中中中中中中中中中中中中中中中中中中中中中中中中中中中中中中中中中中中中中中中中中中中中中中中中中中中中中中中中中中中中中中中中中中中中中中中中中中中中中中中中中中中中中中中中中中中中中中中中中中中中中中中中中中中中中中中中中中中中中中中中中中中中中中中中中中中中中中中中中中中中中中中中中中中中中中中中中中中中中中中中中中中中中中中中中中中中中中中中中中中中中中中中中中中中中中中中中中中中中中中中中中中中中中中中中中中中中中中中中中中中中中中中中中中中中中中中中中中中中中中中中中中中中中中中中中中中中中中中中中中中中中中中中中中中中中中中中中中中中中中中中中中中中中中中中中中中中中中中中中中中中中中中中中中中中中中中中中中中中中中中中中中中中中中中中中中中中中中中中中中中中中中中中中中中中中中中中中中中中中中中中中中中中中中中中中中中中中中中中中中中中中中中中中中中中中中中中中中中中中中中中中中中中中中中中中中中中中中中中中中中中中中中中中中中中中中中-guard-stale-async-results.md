---
title: Guard stale async results
description: When a hook kicks off an async operation (API call, debounced state update,
  subscription callback) whose result is applied later, guard against that result
  landing after the component has moved on — remounted, navigated away and back, or
  received a newer event. Capture a generation/identity token (or the current value
  of the relevant ref/state) before...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: React
language: TypeScript
comments_count: 3
repository_stars: 70986
---

When a hook kicks off an async operation (API call, debounced state update, subscription callback) whose result is applied later, guard against that result landing after the component has moved on — remounted, navigated away and back, or received a newer event. Capture a generation/identity token (or the current value of the relevant ref/state) before starting the async work, and re-check it when the result arrives; only apply the side effect or dispatch if it still matches. Do not let a stale closure-captured ref decide behavior for a component instance that has since been retired.

For example, in `useComposerSuggestions`, `invoke` captures `generationRef.current` before awaiting, and only dispatches the reply if the generation hasn't changed:
```ts
const generation = generationRef.current;
const result = await invokeFor(targetSessionId, action);
if (generation !== generationRef.current) return undefined; // stale: ignore
dispatch({ type: "reply", sessionId: targetSessionId, result, now: Date.now() });
```
The same discipline was missing in `usePromptDraft`/`ChatThreadPane.handleSend`, where a retired pane's `await sendPrompt` continuation used its own stale ref to decide whether to restore a failed prompt, overwriting a newer draft typed in a remounted pane. The fix must validate the current draft/thread lifetime before restoring, not rely on the retired instance's captured ref.

This also applies to combining multiple async-derived flags into one visibility/condition: when one of the inputs is itself a transient signal arriving through a separate stream (e.g., a `cloud_provisioning` message arriving before a debounced state acknowledgement), the combined condition must explicitly account for that transient state everywhere it's used, not just in one helper — otherwise a race window produces incorrect UI (e.g., the loader flashing instead of staying suppressed).

When reviewing hooks with async effects or callbacks:
- Capture and check a generation/version token, or validate current ref/state relevance, before applying any async result.
- When combining multiple derived booleans/state signals, ensure every transient signal is accounted for in every place the combined condition is evaluated.
- Add regression tests that specifically exercise the race: trigger the async action, change identity/state (navigate away and back, remount, emit a newer event), then let the async result resolve, and assert the stale result was ignored.