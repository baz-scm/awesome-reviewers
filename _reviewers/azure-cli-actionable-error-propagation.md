---
title: Actionable Error Propagation
description: When handling failures, ensure your code (a) raises the right exception
  to control exit code/automation, (b) doesn’t silently ignore user intent or skip
  required checks, and (c) produces parameter-aware, actionable messages.
repository: Azure/azure-cli
label: Error Handling
language: Python
comments_count: 18
repository_stars: 4592
---

When handling failures, ensure your code (a) raises the right exception to control exit code/automation, (b) doesn’t silently ignore user intent or skip required checks, and (c) produces parameter-aware, actionable messages.

Practical standards:
1) Explicit success/failure contract
- If any operation truly failed, raise an exception (not just logs) so callers get a non-zero exit code.
- Don’t emit “success-shaped” output before raising.

2) Use precise, intentional exception types
- Use usage/validation-specific errors for user input problems (e.g., ArgumentUsageError / ValidationError / MutuallyExclusiveArgumentError / RequiredArgumentMissingError).
- Catch only expected exceptions; re-raise or let unexpected failures surface (don’t broad-suppress).

3) Make messages context-rich and branch-correct
- For expected “Not Found” or missing-feature scenarios, tailor the message based on which parameters were supplied (e.g., include the missing instance name vs “feature not rolled out”).
- If the SDK error is too generic, re-raise with the specific resource/parameter that caused it.

4) Avoid silent ignores and skipped validations
- If a flag is provided but inapplicable, reject it (or warn clearly) instead of proceeding with a different scope.
- In test/retry/validation flows, never let required checks be skipped in ways that still mark the run as passed—fail loudly.

5) Defensive error detection
- Prefer explicit thresholds (e.g., treat HTTP >= 400 as error) rather than vague truthiness checks.
- Guard exception paths to avoid secondary failures (e.g., undefined variables).

Example pattern (parallel execute with non-zero on failures):
```python
results = run_parallel(...)
failed = [r for r in results if r.get('status') == 'failed']
if failed:
    raise AzureResponseError(
        f"Command execution failed on {len(failed)} of {len(results)} instance(s). "
        "See the messages above for details."
    )
return results  # only when everything was accepted
```

Example pattern (404 messaging that depends on inputs):
```python
if response.status_code == 404:
    if instance:
        raise CLIError(f"No startup logs found for instance '{instance}'. Run list to see available instances.")
    logger.warning("Startup logs are not available for this app; feature may not be rolled out yet.")
    return []
```

Applying these consistently will make CLI behavior predictable for both humans and automation, and will prevent misleading/opaque failures.