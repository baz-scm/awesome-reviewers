---
title: validate IPC inputs
description: Always validate and sanitize inputs to IPC handlers to prevent unauthorized
  access to system resources. Implement allowlists or blocklists for file system operations
  and maintain secure Electron configuration.
repository: block/goose
label: Security
language: TypeScript
comments_count: 2
repository_stars: 19037
---

Always validate and sanitize inputs to IPC handlers to prevent unauthorized access to system resources. Implement allowlists or blocklists for file system operations and maintain secure Electron configuration.

IPC handlers that accept file paths, URLs, or other system resources can be exploited if not properly validated. Even with secure Electron configuration (context isolation enabled, node integration disabled), IPC endpoints remain potential attack vectors.

Example of vulnerable code:
```typescript
ipcMain.handle('open-directory-in-explorer', async (_event, path: string) => {
  // Dangerous: path can be any directory on the machine
  shell.openPath(path);
});
```

Secure implementation:
```typescript
const ALLOWED_DIRECTORIES = ['/safe/app/directory', '/user/documents'];

ipcMain.handle('open-directory-in-explorer', async (_event, path: string) => {
  // Validate path is in allowlist
  const normalizedPath = path.normalize(path);
  if (!ALLOWED_DIRECTORIES.some(allowed => normalizedPath.startsWith(allowed))) {
    throw new Error('Directory access not permitted');
  }
  shell.openPath(normalizedPath);
});
```

Ensure your Electron app maintains secure configuration: context isolation enabled, node integration disabled, web security enabled, and controlled API surface through preload scripts with explicit method exposure.