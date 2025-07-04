---
title: Validate user-controlled paths
description: Always validate and sanitize user-provided inputs used in file path operations
  to prevent path traversal attacks. Path traversal vulnerabilities can allow attackers
  to access unauthorized files outside the intended directory structure.
repository: apache/airflow
label: Security
language: Python
comments_count: 6
repository_stars: 40858
---

Always validate and sanitize user-provided inputs used in file path operations to prevent path traversal attacks. Path traversal vulnerabilities can allow attackers to access unauthorized files outside the intended directory structure.

Key implementation steps:
1. URL decode the input to handle encoded traversal attempts
2. Check for control characters and null bytes
3. Normalize paths and resolve symbolic links
4. Verify the resolved path stays within the allowed directory
5. Validate the file type before access

Example implementation:
```python
def _validate_log_file_path(filename: str, log_directory: str) -> Path:
    """
    Validate that the requested file path is within the log directory and safe to serve.
    """
    # URL decode the filename to handle encoded path traversal attempts
    try:
        decoded_filename = urllib.parse.unquote(filename)
    except Exception as e:
        logger.warning("Failed to URL decode filename '%s': %s", filename, e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL encoding in filename",
        )

    # Check for control characters and null bytes
    if not decoded_filename or any(ord(c) < 32 for c in decoded_filename):
        logger.warning("Invalid characters detected in filename")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid characters in filename",
        )
    if "\x00" in decoded_filename:
        logger.warning("Null byte detected in filename")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Null byte in filename",
        )

    # Normalize paths and verify they remain within allowed directory
    log_dir = Path(log_directory).resolve()
    file_path = log_dir / decoded_filename
    resolved_path = file_path.resolve()
    
    if not resolved_path.is_relative_to(log_dir):
        logger.warning("Path traversal attempt detected")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: path outside log directory",
        )

    # Verify file type (not a directory or special file)
    if resolved_path.exists() and not resolved_path.is_file():
        logger.warning("Attempt to access non-file resource")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not a regular file",
        )
        
    return resolved_path
```

For security best practices, avoid logging the actual path contents in error messages to clients. Only log detailed error information server-side to avoid providing attackers with information that could help refine their attacks.