---
title: Secure before deployment
description: Remove or secure development-specific code before deploying to production
  environments. Development artifacts like debug print statements, weak validation
  methods, and development endpoints can introduce significant security vulnerabilities.
repository: vllm-project/vllm
label: Security
language: Python
comments_count: 3
repository_stars: 51730
---

Remove or secure development-specific code before deploying to production environments. Development artifacts like debug print statements, weak validation methods, and development endpoints can introduce significant security vulnerabilities.

Specifically:
1. Remove all debugging print statements that might leak sensitive request data, credentials, or tokens
2. Implement thorough validation for security-critical functions, considering bypass techniques (e.g., symbolic links in command validation)
3. Ensure development features have proper warnings and automated tests to verify they're not accidentally enabled in production

Example of insecure code:
```python
@router.post("/v1/responses")
async def create_responses(request: ResponsesRequest, raw_request: Request):
    print(request, raw_request)  # INSECURE: Leaks sensitive data to logs
    
def is_dangerous_cmd(cmd):
    cmd_base = os.path.basename(cmd)  # INSECURE: Can be bypassed with symlinks
    return cmd_base in COMMAND_BLACKLIST
```

Example of secure code:
```python
@router.post("/v1/responses")
async def create_responses(request: ResponsesRequest, raw_request: Request):
    # Debug statements removed for production
    
def is_dangerous_cmd(cmd):
    # Resolve any symlinks to get the real path
    real_path = os.path.realpath(cmd)
    cmd_base = os.path.basename(real_path)
    return cmd_base in COMMAND_BLACKLIST
    
# When enabling development features:
if envs.VLLM_SERVER_DEV_MODE:
    logger.warning("SECURITY WARNING: Development endpoints are enabled!")
    # Accompany with tests to verify this warning is present
```