---
title: Prevent command injection
description: Always use child_process.spawn() with array arguments instead of exec()
  with string concatenation when executing system commands. This prevents command
  injection vulnerabilities that can occur when untrusted input is incorporated into
  command strings.
repository: openai/codex
label: Security
language: TSX
comments_count: 1
repository_stars: 31275
---

Always use child_process.spawn() with array arguments instead of exec() with string concatenation when executing system commands. This prevents command injection vulnerabilities that can occur when untrusted input is incorporated into command strings.

**Problematic code:**
```typescript
const safePreview = preview.replace(/"/g, '\\"');
const title = "Codex CLI";
exec(`osascript -e "display notification \\"${safePreview}\\" with title \\"${title}\\""`, { cwd });
```

**Secure code:**
```typescript
const title = "Codex CLI";
spawn('osascript', [
  '-e',
  `display notification "${preview}" with title "${title}"`
], { cwd });
```

By passing arguments as separate array elements, the operating system receives them without interpreting special characters as command syntax, ensuring untrusted input cannot escape its intended context.