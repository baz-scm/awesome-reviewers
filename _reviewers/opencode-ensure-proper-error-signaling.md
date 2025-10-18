---
title: Ensure proper error signaling
description: Errors must be communicated through appropriate mechanisms for their
  execution context. In CLI applications, use proper exit codes to indicate error
  states (non-zero for failures). For shell command execution, implement proper error
  handling to prevent unexpected crashes and provide graceful failure modes.
repository: sst/opencode
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 28213
---

Errors must be communicated through appropriate mechanisms for their execution context. In CLI applications, use proper exit codes to indicate error states (non-zero for failures). For shell command execution, implement proper error handling to prevent unexpected crashes and provide graceful failure modes.

For CLI tools, always set appropriate exit codes when errors occur:
```typescript
if (err) {
  spinner.stop("Upgrade failed", 1) // Exit code 1 for error
  // ... handle error logging
}
```

For shell commands, use error handling mechanisms like `.quiet().nothrow()` to prevent crashes:
```typescript
await $`curl -L -o '${archivePath}' '${releaseURL}'`.quiet().nothrow()
await $`tar -xzf ${archivePath}`.cwd(distPath).quiet().nothrow()
```

This ensures that errors are properly signaled to the appropriate layer (operating system, calling process, or user interface) and prevents silent failures or unexpected crashes.