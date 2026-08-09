---
title: Redact All Logs
description: Security diagnostic output must not leak sensitive data. If you enable
  verbose modes (e.g., `--verbose`) or change log sinks (stdout vs stderr), ensure
  (and document) that *all* emitted diagnostic streams are actually redacted.
repository: openai/codex-security
label: Security
language: Markdown
comments_count: 1
repository_stars: 9394
---

Security diagnostic output must not leak sensitive data. If you enable verbose modes (e.g., `--verbose`) or change log sinks (stdout vs stderr), ensure (and document) that *all* emitted diagnostic streams are actually redacted.

How to apply:
- **Align claims with behavior:** Don’t state “provider messages are redacted” unless you’ve verified it for **stderr and stdout**.
- **Test both streams:** In CI, capture both outputs and assert sensitive fields (tenant IDs, request details, raw provider messages) do not appear.
- **Fail closed:** If redaction can’t be guaranteed for a stream, either redact it before printing or narrow the documentation/feature to avoid misleading users.

Example (test assertion pattern):
```js
const child = spawn('npx', ['@openai/codex-security', 'scan', '.', '--verbose']);
let stdout = '', stderr = '';
child.stdout.on('data', d => (stdout += d));
child.stderr.on('data', d => (stderr += d));

await once(child, 'close');

// Assert nothing sensitive leaked to either stream
for (const s of [stdout, stderr]) {
  expect(s).not.toMatch(/tenant/i);
  expect(s).not.toMatch(/request/i);
  expect(s).not.toMatch(/raw provider/i);
}
```

This prevents verbose/security diagnostics from becoming an unintended data-exfiltration channel (especially through stderr).