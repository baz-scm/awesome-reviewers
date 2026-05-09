---
title: Error precedence and degradation
description: When implementing error handling, ensure (1) failures are validated early
  or handled explicitly, (2) optional steps degrade gracefully, (3) cancellation/abort
  prevents unnecessary work, and (4) cleanup never masks the true result.
repository: coleam00/Archon
label: Error Handling
language: TypeScript
comments_count: 7
repository_stars: 21089
---

When implementing error handling, ensure (1) failures are validated early or handled explicitly, (2) optional steps degrade gracefully, (3) cancellation/abort prevents unnecessary work, and (4) cleanup never masks the true result.

Practical rules:
1) Fail fast on invalid configuration
- Validate env/config values before spawning subprocesses or performing I/O.
- Throw actionable errors with the offending value and where to fix it.

2) Use safe fallbacks when detection/lookup can be uncertain
- Only override defaults when you’re confident in the result; otherwise keep backward-compatible defaults.

3) Treat optional capabilities as non-fatal
- Gate optional actions behind preconditions (e.g., “only run if .gitmodules exists”).
- Catch failures, log a warning, and continue the primary workflow.

4) Respect abort/cancellation as an explicit control flow
- If abortSignal is already aborted, return/throw immediately (do not start expensive work).

5) Preserve error precedence during cleanup
- Always perform cleanup in a `finally` block.
- If cleanup fails, log it, but do not replace the primary error/result.

6) Don’t emit misleading secondary errors/warnings
- If the system provides a fallback success path after an error event, suppress spurious warnings that would confuse operators.

Example (pattern):
```ts
async function runWithPreflightAndCleanup(opts: {
  abortSignal?: AbortSignal;
  envOverrides?: Record<string, string>;
}) {
  if (opts.abortSignal?.aborted) {
    throw Object.assign(new Error('Aborted'), { name: 'AbortError' });
  }

  const prev = new Map<string, string | undefined>();
  let primaryError: unknown;

  try {
    // Preflight validation (fail fast)
    const binary = opts.envOverrides?.COPILOT_BIN_PATH;
    if (binary !== undefined && binary.trim() === '') {
      throw new Error('COPILOT_BIN_PATH is set but blank');
    }

    // Optional step (non-fatal)
    try {
      await maybeOptionalStep();
    } catch (err) {
      logger.warn({ err }, 'optional_step_failed');
    }

    // Primary work
    return await doPrimaryWork();
  } catch (err) {
    primaryError = err;
    throw err;
  } finally {
    // Cleanup must not mask primary outcome
    try {
      if (opts.envOverrides) {
        for (const [k, v] of Object.entries(opts.envOverrides)) {
          if (prev.has(k)) {
            const old = prev.get(k);
            if (old === undefined) Reflect.deleteProperty(process.env, k);
            else process.env[k] = old;
          }
        }
      }
    } catch (cleanupErr) {
      logger.warn({ cleanupErr }, 'cleanup_failed');
      // never replace/override primaryError
    }
  }
}
```