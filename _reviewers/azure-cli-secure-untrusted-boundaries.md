---
title: Secure Untrusted Boundaries
description: 'When code crosses security boundaries (subprocess/PowerShell execution,
  network URLs, filesystem writes, or auth/TLS), treat user/environment input as untrusted
  and enforce safety rules:'
repository: Azure/azure-cli
label: Security
language: Python
comments_count: 8
repository_stars: 4592
---

When code crosses security boundaries (subprocess/PowerShell execution, network URLs, filesystem writes, or auth/TLS), treat user/environment input as untrusted and enforce safety rules:

- Subprocess/PowerShell: never rely on naive quoting/concatenation. Pass arguments as separate items, and ensure the resulting command string cannot be interpreted as executable/injected content.
- Secret handling: don’t echo or log raw user-provided command strings (or anything credential-like). If logging is needed, redact/summarize.
- Executable resolution: resolve intended binaries from PATH to an absolute, normalized path before calling subprocess; avoid current-directory fallbacks (especially on Windows).
- Filesystem: refuse dangerous targets (e.g., symlinks) and perform atomic writes via a temp file + replace; set/adjust permissions appropriately.
- Network/auth: enforce secure TLS verification defaults for authentication flows; don’t honor “disable verification” env vars for auth. For network-isolated environments, validate/deny forbidden URL patterns precisely.
- Forward/escape hatch commands: if you must pass through to another CLI (or service), clearly document the trust boundary and validate/limit inputs where possible.

Example (PowerShell injection-safe pattern):
```python
# Avoid building -Command strings with unsafe quoting.
# Prefer passing the URL as a separate argument, not interpolated into a quoted executable string.
return subprocess.Popen(
    ['powershell.exe', '-NoProfile', '-Command', 'Start-Process', url]
).wait()
```

Example (safe kubeconfig write):
```python
if os.path.islink(existing_path):
    raise CLIError('Refusing to write to symlink target.')
parent = os.path.dirname(existing_path) or '.'
tmp_fd, tmp_path = tempfile.mkstemp(dir=parent)
try:
    with os.fdopen(tmp_fd, 'w') as f:
        yaml.safe_dump(data, f)
    os.chmod(tmp_path, 0o600)
    os.replace(tmp_path, existing_path)
finally:
    # handle cleanup if needed
    pass
```

Apply this standard in code reviews by asking: (1) What untrusted data is reaching a command string, URL, or file path? (2) Is it validated/sanitized/escaped correctly? (3) Are secrets redacted in logs/output? (4) Are there protections against path/symlink and unintended binary execution? (5) Are auth/TLS and URL restrictions enforced safely?