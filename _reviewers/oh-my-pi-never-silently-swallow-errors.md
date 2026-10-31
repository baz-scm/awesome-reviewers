---
title: Never silently swallow errors
description: 'Empty `catch {}` blocks hide real failures and make debugging impossible;
  several reviews found bugs that existed only because a failure path logged nothing.
  Treat every catch as a decision point, not a place to discard information:'
repository: can1357/oh-my-pi
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 37317
---

Empty `catch {}` blocks hide real failures and make debugging impossible; several reviews found bugs that existed only because a failure path logged nothing. Treat every catch as a decision point, not a place to discard information:

1. **Never leave a catch block empty.** Log the error with enough context (operation, identifiers, `error.message`) so a future failure is diagnosable, unless the condition is a genuinely expected race that is explicitly documented as such.
2. **Distinguish expected contention from real failure.** Blindly adding `logger.warn` to every catch produces noise for ordinary races (e.g. `ENOENT` because another process already removed a lock/file). Check for the known benign error code first and return/continue quietly; reserve `warn`/`error` logs for failures that actually need attention:
   ```ts
   try {
     await fs.rm(lockDir, { recursive: true, force: true });
   } catch (error) {
     if (isEnoent(error)) return; // another holder already cleaned it up
     logger.warn("failed to release lock dir", { lockDir, error: String(error) });
   }
   ```
3. **Never let a secondary (cleanup/reporting) failure mask the primary one.** When a catch block performs cleanup or calls a user-supplied error callback, wrap that secondary action in its own try/catch, log if it fails, and still surface/propagate the original error — don't let the cleanup's exception replace it or disappear silently.
   ```ts
   const reportError = (error: Error): void => {
     if (reported) return;
     reported = true;
     try {
       onError?.(error);
     } catch (hookError) {
       logger.warn("error handler itself threw", { error: String(hookError) });
     }
   };
   try {
     await op();
   } catch (error) {
     reportError(toError(error)); // original error is still the one reported
   }
   ```
4. **Honor "never rejects" / "report once" contracts consistently.** If an API promises it never rejects (e.g. to avoid an unhandled rejection crashing the host), every code path implementing that API — not just the first one patched — must funnel through the same guarded reporter, and that reporter itself must be exception-safe.

Applying these rules turns a swallowed failure into either a traceable log line or a correctly-propagated error, and prevents unrelated secondary failures from hiding the root cause.