---
title: Shell-specific input escaping
description: When processing user input that will be used in shell commands, implement
  shell-specific escaping mechanisms to prevent command injection vulnerabilities.
  Different shells (bash, PowerShell, zsh, fish) have different escaping requirements
  that must be handled appropriately.
repository: microsoft/vscode
label: Security
language: TypeScript
comments_count: 1
repository_stars: 174887
---

When processing user input that will be used in shell commands, implement shell-specific escaping mechanisms to prevent command injection vulnerabilities. Different shells (bash, PowerShell, zsh, fish) have different escaping requirements that must be handled appropriately.

For example, instead of using a generic approach like:
```typescript
// Unsafe - generic character removal
const bannedChars = /[\`\$\|\&\>\~\#\!\^\*\;\<\"\']/g;
newPath = newPath.replace(bannedChars, '');
```

Implement shell-specific escaping:
```typescript
// Safe - proper shell-specific escaping
if (shellType === 'bash' || shellType === 'zsh') {
  // POSIX-compliant escaping for single quotes
  if (path.includes("'")) {
    path = path.replace(/'/g, "'\\''");
  }
} else if (shellType === 'fish') {
  // Fish uses backslash escaping
  if (path.includes("'")) {
    path = path.replace(/'/g, "\\'");
  }
} else if (shellType === 'powershell') {
  // PowerShell uses doubled single quotes
  if (path.includes("'")) {
    path = path.replace(/'/g, "''");
  }
}
```

This approach prevents security vulnerabilities by ensuring that user input cannot break out of string contexts to execute arbitrary commands.