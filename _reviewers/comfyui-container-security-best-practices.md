---
title: Container security best practices
description: Implement comprehensive security measures in containerized applications
  to prevent privilege escalation, injection attacks, and unauthorized access. This
  includes proper user configuration, variable quoting, and secure process handling.
repository: comfyanonymous/ComfyUI
label: Security
language: Dockerfile
comments_count: 2
repository_stars: 83726
---

Implement comprehensive security measures in containerized applications to prevent privilege escalation, injection attacks, and unauthorized access. This includes proper user configuration, variable quoting, and secure process handling.

Key security practices:

1. **Use secure user IDs**: Use UID/GID 999 (standard for official images) instead of 1000 to reduce container escape risks
2. **Quote shell variables**: Always quote variables in shell commands to prevent injection attacks
3. **Implement proper file permissions**: Use restrictive umask (0077) to limit file access to owner only
4. **Handle process switching securely**: Use `setpriv` for secure user switching and `exec` for proper signal handling

Example of secure variable quoting:
```dockerfile
# Vulnerable - unquoted variables
CMD python -u main.py --listen ${COMFYUI_ADDRESS} --port ${COMFYUI_PORT}

# Secure - quoted variables  
CMD python -u main.py --listen "${COMFYUI_ADDRESS}" --port "${COMFYUI_PORT}"
```

Example of secure user configuration:
```dockerfile
# Use standard secure UID/GID
ARG USER_UID=999
ARG USER_GID=999

# Create system user with restricted permissions
RUN adduser --system --home /home/user --uid ${USER_UID} --group user
```

These practices significantly reduce attack surface and prevent common container security vulnerabilities.