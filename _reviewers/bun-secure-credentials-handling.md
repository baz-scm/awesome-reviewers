---
title: Secure credentials handling
description: When handling credentials or secrets in code, avoid passing them directly
  through command substitution or template literals in shell commands, as this can
  lead to security vulnerabilities. Instead, write sensitive data to temporary files
  with restricted permissions, use those files for operations requiring credentials,
  and ensure proper cleanup afterward.
repository: oven-sh/bun
label: Security
language: TypeScript
comments_count: 1
repository_stars: 79093
---

When handling credentials or secrets in code, avoid passing them directly through command substitution or template literals in shell commands, as this can lead to security vulnerabilities. Instead, write sensitive data to temporary files with restricted permissions, use those files for operations requiring credentials, and ensure proper cleanup afterward.

Example:
```ts
// Insecure way - potential command injection or exposure risk
await Bun.$`bash -c 'age -d -i <(echo "$AGE_CORES_IDENTITY")' < ${cores} | tar -zxvC ${dir}`;

// Secure way - controlled lifecycle for sensitive data
const identityFile = join(dir, "identity.key");
await Bun.write(identityFile, process.env.AGE_CORES_IDENTITY);
await Bun.chmod(identityFile, 0o600); // Restrict file permissions
await Bun.$`age -d -i ${identityFile} < ${cores} | tar -zxvC ${dir}`;
await Bun.rm(identityFile); // Clean up the sensitive file
```

This approach prevents credential leakage through command history, process lists, or insecure file permissions, and ensures sensitive data is promptly removed after use.