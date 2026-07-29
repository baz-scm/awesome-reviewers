---
title: Error semantics invariants
description: When handling failures, treat “what happened” as a precise, testable
  contract—not an interpretation. Ensure (1) classification predicates are exact and
  consistent across docs+code, (2) failure causes are not overloaded, (3) cleanup/settlement
  invariants prevent stranded states, and (4) adapter/step contracts are enforced
  with safe fallbacks.
repository: QwenLM/qwen-code
label: Error Handling
language: Markdown
comments_count: 6
repository_stars: 26407
---

When handling failures, treat “what happened” as a precise, testable contract—not an interpretation. Ensure (1) classification predicates are exact and consistent across docs+code, (2) failure causes are not overloaded, (3) cleanup/settlement invariants prevent stranded states, and (4) adapter/step contracts are enforced with safe fallbacks.

Apply these rules:

1) Freeze exact recovery predicates (spec == code)
- Define the exact conditions for each outcome (e.g., exit code 1 = no matches) and keep design docs aligned with implementation.
- Avoid adding “extra” checks unless you’ve proven they are correct for all modes (e.g., JSON summary events that change stdout).

2) Carry failure cause explicitly; never infer from an overloaded signal
- If you use an abort signal, you must also carry a typed reason and map it to the correct terminal state (e.g., cross-surface answer vs host/request destruction).
- Ensure status transitions remain consistent between components (question card vs status card).

3) Enforce exactly-once settlement and all parallel invariants
- If you remove/settle one pending entity, you must also update any related tracking structures (e.g., per-run pending request sets) on every terminal path.
- Make the invariant executable (assertions in code/tests), not just descriptive.

4) Validate “handled”/“presented” contracts; on violation, fall back to safe path
- If an adapter returns `handled` but didn’t perform the required settlement action (e.g., calling `respond()`), treat it as `unsupported` and continue the normal fallback so the request cannot get stuck.

Example (pseudocode)
```ts
// 1) Exact error classification predicate
function classifyNoMatches(rg: { exitCode: number; stdout: string; stderr: string }) {
  // NO MATCHES only when exitCode==1 and stderr is empty.
  // (Do not key off stdout; JSON modes may emit stdout summaries.)
  if (rg.exitCode === 1 && rg.stderr.length === 0) return 'no_matches';
  return 'not_no_matches';
}

// 2) Adapter contract enforcement
async function presentWithContract(ctx: {
  presentUserInputRequest: () => Promise<'presented'|'handled'|'unsupported'>;
  respondMustBeCalledForHandled: () => void;
}) {
  let respondCalled = false;
  const wrappedRespond = () => { respondCalled = true; ctx.respondMustBeCalledForHandled(); };

  const result = await ctx.presentUserInputRequest(/* uses wrappedRespond */);

  if (result === 'handled' && !respondCalled) {
    // Contract broken: fall through to existing permission formatter/sender.
    return 'unsupported';
  }
  return result;
}

// 3) Typed settlement reasons (conceptual)
// settlementSignal.reason must distinguish answered_elsewhere vs request_cancelled/run_cancelled/expired.
```

Checklist before merge
- [ ] Are the outcome predicates documented and identical to code?
- [ ] Is every failure mode mapped to a distinct typed reason (no overloaded abort semantics)?
- [ ] Does every terminal path update *all* invariants/registries (no stranded waiting states)?
- [ ] Are “handled/presented” contracts enforced with runtime guards that trigger safe fallbacks?
- [ ] Does the degradation table cover every step (e.g., “create succeeded but streaming-open failed”)?
