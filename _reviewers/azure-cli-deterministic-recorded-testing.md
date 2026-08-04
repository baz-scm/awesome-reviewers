---
title: Deterministic recorded testing
description: For scenario/recording tests, keep behavior deterministic between record
  and replay, and ensure assertions cover defaults, required inputs, and optional
  fields.
repository: Azure/azure-cli
label: Testing
language: Python
comments_count: 8
repository_stars: 4592
---

For scenario/recording tests, keep behavior deterministic between record and replay, and ensure assertions cover defaults, required inputs, and optional fields.

Apply these rules:
- Validate default/update semantics: add scenario tests for “not provided” and “explicit value” (including update preserving existing state).
- Add negative coverage for required arguments and pin expected error messages.
- Cover optional fields in the constructed model/payload (don’t only assert with None).
- Prevent cassette mismatches:
  - Avoid runtime-generated random names in tests that rely on committed recordings.
  - Use neutral placeholders + scrubbed cassettes, and keep env-var overrides only for live re-recording.
- If you add live-only stabilization (poll/retry/waits):
  - Ensure the logic only runs in live mode.
  - Do not commit recordings created with the live-only flag/wait behavior.
  - Skip any sleep/wait in replay mode.

Example (live-only polling adapter pattern):
```python
def cmd(self, command, checks=None, expect_failure=False):
    if self.is_live and os.environ.get('AZURE_CLI_TEST_RETRY_PROVISIONING_CHECK') == 'true':
        return self._cmd_with_retry(command, checks, expect_failure)
    # replay path uses normal ScenarioTest.cmd so it matches the cassette
    return super().cmd(command, checks=checks, expect_failure=expect_failure)
```

If a test can’t be made deterministic (e.g., it generates a new resource name each run), mark it `@live_only()` and remove the stale recordings rather than trying to force replay to match changing values.