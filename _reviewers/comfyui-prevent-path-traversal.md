---
title: Prevent path traversal
description: Always validate and sanitize file paths from user input to prevent directory
  traversal attacks. Malicious actors can use path manipulation techniques like `../../../`
  sequences or absolute paths to access files outside intended directories, potentially
  overwriting critical system files or accessing sensitive data.
repository: comfyanonymous/ComfyUI
label: Security
language: Python
comments_count: 3
repository_stars: 83726
---

Always validate and sanitize file paths from user input to prevent directory traversal attacks. Malicious actors can use path manipulation techniques like `../../../` sequences or absolute paths to access files outside intended directories, potentially overwriting critical system files or accessing sensitive data.

Key validation steps:
1. Sanitize input by removing or rejecting dangerous path components
2. Resolve the full absolute path and verify it stays within allowed boundaries
3. Validate both directory and filename components separately

Example of vulnerable code:
```python
# BAD: No validation allows path traversal
model_name = user_input  # Could be "../../../../passwd"
file_path = os.path.join(models_dir, model_sub_directory, model_name)
```

Example of secure implementation:
```python
# GOOD: Validate filename and check final path
def validate_filename(filename):
    # Reject dangerous characters and sequences
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    return True

if not validate_filename(model_name):
    raise ValueError("Invalid filename")

file_path = os.path.join(models_dir, model_sub_directory, model_name)
resolved_path = os.path.abspath(file_path)

# Ensure final path is within allowed directory
if not resolved_path.startswith(os.path.abspath(models_dir)):
    raise ValueError("Path outside allowed directory")
```

This prevents attackers from writing malicious code to locations like `custom_nodes/*/.__init__.py` or accessing sensitive system directories.