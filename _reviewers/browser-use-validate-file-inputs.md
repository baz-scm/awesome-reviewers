---
title: validate file inputs
description: All file-related operations must implement comprehensive input validation
  and sanitization to prevent path traversal attacks, arbitrary file system access,
  and execution of malicious content. This is especially critical when handling user-provided
  file paths or when systems interact with AI agents that could be manipulated through
  prompt injection.
repository: browser-use/browser-use
label: Security
language: Python
comments_count: 3
repository_stars: 69139
---

All file-related operations must implement comprehensive input validation and sanitization to prevent path traversal attacks, arbitrary file system access, and execution of malicious content. This is especially critical when handling user-provided file paths or when systems interact with AI agents that could be manipulated through prompt injection.

Key validation requirements:
- **Filename sanitization**: Strip all non-alphanumeric characters except spaces, underscores, and hyphens. Replace invalid characters with underscores. Limit filenames to 64 characters maximum.
- **Extension restrictions**: Only allow specific safe file extensions (e.g., `.txt`, `.pdf`) based on the use case.
- **Path traversal prevention**: Reject any paths containing `..`, `/`, or `\` characters. Validate that paths don't resolve to dangerous system directories.
- **Directory restrictions**: Explicitly block access to sensitive directories like `/`, `~`, `~/Desktop`, `~/Documents`. Restrict operations to dedicated safe directories or current working directory.
- **Executable prevention**: Check for script indicators like `#!` at file start and verify no executable permission bits are set after file creation.

Example implementation:
```python
def validate_file_path(file_path: str, allowed_extensions: list[str]) -> str:
    # Check for dangerous directories
    dangerous_paths = ['/', '~', '~/Desktop', '~/Documents']
    if file_path in dangerous_paths:
        raise ValueError(f"Access to {file_path} is not allowed")
    
    # Extract filename and validate
    filename = Path(file_path).name
    
    # Sanitize filename
    sanitized = re.sub(r'[^a-zA-Z0-9 _-]', '_', filename)
    if len(sanitized) > 64:
        sanitized = sanitized[:64]
    
    # Check extension
    if not any(sanitized.endswith(ext) for ext in allowed_extensions):
        raise ValueError(f"File extension not allowed: {sanitized}")
    
    return sanitized
```

This prevents AI agents or malicious users from writing to system files, executing scripts, or accessing sensitive directories through path traversal attacks.