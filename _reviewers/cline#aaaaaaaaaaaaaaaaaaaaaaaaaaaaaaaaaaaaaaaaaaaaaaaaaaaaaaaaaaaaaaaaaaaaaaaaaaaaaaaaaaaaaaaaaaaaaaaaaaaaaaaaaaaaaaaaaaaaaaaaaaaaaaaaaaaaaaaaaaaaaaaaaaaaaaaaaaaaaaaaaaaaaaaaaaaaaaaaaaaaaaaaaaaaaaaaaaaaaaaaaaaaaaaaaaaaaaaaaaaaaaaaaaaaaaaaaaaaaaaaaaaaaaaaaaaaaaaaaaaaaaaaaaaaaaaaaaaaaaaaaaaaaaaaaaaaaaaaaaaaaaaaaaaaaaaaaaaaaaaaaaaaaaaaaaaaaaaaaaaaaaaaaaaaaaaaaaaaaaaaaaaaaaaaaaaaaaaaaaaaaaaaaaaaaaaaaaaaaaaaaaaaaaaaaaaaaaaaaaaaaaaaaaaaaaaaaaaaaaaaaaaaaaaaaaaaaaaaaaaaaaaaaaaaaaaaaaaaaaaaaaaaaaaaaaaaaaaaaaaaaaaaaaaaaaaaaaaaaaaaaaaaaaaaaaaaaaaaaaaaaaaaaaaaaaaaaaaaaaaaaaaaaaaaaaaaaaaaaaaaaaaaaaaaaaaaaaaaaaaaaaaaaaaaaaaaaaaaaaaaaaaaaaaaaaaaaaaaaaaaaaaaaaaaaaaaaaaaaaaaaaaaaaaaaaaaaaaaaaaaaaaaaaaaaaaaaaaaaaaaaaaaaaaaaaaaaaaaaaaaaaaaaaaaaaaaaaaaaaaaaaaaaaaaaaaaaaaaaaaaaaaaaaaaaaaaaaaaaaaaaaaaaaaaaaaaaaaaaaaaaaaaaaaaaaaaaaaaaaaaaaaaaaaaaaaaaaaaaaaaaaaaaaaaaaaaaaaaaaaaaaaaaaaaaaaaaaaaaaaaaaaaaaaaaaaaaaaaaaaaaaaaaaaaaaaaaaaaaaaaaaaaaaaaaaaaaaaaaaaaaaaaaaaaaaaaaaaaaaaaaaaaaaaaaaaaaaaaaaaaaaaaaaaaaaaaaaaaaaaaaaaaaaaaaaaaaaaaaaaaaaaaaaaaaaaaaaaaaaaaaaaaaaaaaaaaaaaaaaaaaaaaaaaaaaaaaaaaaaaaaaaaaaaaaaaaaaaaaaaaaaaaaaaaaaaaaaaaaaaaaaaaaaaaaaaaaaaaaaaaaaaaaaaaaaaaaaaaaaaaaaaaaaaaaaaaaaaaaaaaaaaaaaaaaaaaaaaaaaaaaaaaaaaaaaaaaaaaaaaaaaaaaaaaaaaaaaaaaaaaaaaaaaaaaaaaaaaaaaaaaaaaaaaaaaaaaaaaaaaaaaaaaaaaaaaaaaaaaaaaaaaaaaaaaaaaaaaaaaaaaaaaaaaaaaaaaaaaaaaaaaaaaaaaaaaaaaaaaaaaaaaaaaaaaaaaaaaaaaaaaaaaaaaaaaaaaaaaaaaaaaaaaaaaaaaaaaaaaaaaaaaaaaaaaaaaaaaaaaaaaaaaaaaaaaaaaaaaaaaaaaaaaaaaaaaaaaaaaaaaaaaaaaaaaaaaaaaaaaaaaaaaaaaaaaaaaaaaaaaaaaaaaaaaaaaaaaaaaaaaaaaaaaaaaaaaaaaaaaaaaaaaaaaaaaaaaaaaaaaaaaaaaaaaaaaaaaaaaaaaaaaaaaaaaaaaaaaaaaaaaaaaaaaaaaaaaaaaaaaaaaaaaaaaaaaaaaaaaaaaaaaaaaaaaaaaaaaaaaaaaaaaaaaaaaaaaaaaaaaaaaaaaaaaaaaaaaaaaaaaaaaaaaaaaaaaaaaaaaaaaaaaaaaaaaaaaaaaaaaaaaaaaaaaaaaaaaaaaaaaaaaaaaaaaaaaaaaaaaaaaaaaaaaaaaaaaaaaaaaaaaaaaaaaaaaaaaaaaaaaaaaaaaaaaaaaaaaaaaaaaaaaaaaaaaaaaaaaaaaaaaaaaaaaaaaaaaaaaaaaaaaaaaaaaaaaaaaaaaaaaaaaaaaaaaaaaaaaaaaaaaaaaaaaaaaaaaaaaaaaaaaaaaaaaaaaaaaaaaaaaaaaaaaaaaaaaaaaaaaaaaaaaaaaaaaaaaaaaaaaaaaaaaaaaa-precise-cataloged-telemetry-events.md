---
title: Precise, cataloged telemetry events
description: 'Telemetry is only useful if it is trustworthy and queryable. Follow
  these rules when adding or changing any capture:


  1. **No raw event strings in scope.** Wherever the event catalog rule applies (core,
  agents, cli, vscode, etc.), define a named constant in the shared `CORE_TELEMETRY_EVENTS`
  catalog plus a typed `captureX` helper, and call the helper...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70970
---

Telemetry is only useful if it is trustworthy and queryable. Follow these rules when adding or changing any capture:

1. **No raw event strings in scope.** Wherever the event catalog rule applies (core, agents, cli, vscode, etc.), define a named constant in the shared `CORE_TELEMETRY_EVENTS` catalog plus a typed `captureX` helper, and call the helper instead of `telemetry.capture({ event: "some.string", ... })`. This keeps event names discoverable, typed, and consistent, and prevents a core catalog entry from drifting from what's actually emitted (e.g. `capturePendingPromptsDiscarded`, `captureSdkStreamRetry`, `captureMarketplaceInstall`).

2. **The reported reason/stage must match the actual triggering condition.** Don't bucket distinct failure modes under one label for convenience — e.g. an empty-output condition is not a `TIMEOUT`, and a generic ask-rejection is not a `STREAM_TIMEOUT`. If a metric needs to distinguish causes, add a dedicated reason/stage value rather than overloading an existing one; otherwise the metric silently loses its diagnostic value.

3. **When renaming/refactoring a captured property, audit every call site.** Positional calls compile fine even when a parameter's meaning changes (e.g. `taskId` silently becoming `ulid`), so a rename can corrupt data without any compiler error. Grep all callers of the changed helper and update them, and prefer named/object parameters for capture helpers to make this class of bug impossible.

4. **Every "started" phase needs a matching terminal phase**, including on thrown/aborted paths. If an operation emits `phase: started`, make sure every exit path (success, handled failure, rethrow, listener throwing) closes it with a terminal phase (`succeeded`/`failed` + an `eventType`) before the function returns or rethrows — otherwise the funnel looks like it never completes.

5. **Derive success/failure from the real outcome, never from "the code ran".** A retry that errors, aborts, or is truncated again is not a success just because the retry path executed. Compute the verdict from the actual finish reason/outcome, and keep that judgement in one place (e.g. the run loop) so telemetry stays purely observational and cannot contradict the thing it's describing.

Example of a correctly closed, cataloged event:
```ts
this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, { phase: "started" });
try {
  const retry = await this.generateAssistantMessage({ overflowRecovery: true });
  const succeeded = retry.finishReason === "stop" || retry.finishReason === "tool-calls";
  this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, {
    phase: succeeded ? "succeeded" : "failed",
    eventType: succeeded ? undefined : retry.finishReason,
  });
} catch (error) {
  this.captureTaskLifecycle(TASK_MAX_TOKENS_RECOVERY_EVENT, {
    phase: "failed",
    eventType: this.isAbortError(error) ? "aborted" : "retry_threw",
  });
  throw error;
}
```