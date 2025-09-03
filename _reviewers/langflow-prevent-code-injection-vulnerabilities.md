---
title: Prevent code injection vulnerabilities
description: When evaluating user-provided code or handling dynamic content, implement
  strict security measures to prevent malicious code execution and unauthorized access.
  This includes whitelisting allowed modules/imports, validating input integrity,
  and properly handling sensitive data.
repository: langflow-ai/langflow
label: Security
language: Python
comments_count: 4
repository_stars: 111046
---

When evaluating user-provided code or handling dynamic content, implement strict security measures to prevent malicious code execution and unauthorized access. This includes whitelisting allowed modules/imports, validating input integrity, and properly handling sensitive data.

Key practices:
1. **Whitelist imports**: Restrict which modules can be imported in user code to prevent access to dangerous functionality
2. **Secure evaluation**: Use safe evaluation methods and validate code integrity before execution
3. **Credential scrubbing**: Clear sensitive data from memory after use and document security measures clearly
4. **Input validation**: Ensure fallback mechanisms don't create security bypasses

Example of secure code evaluation:
```python
# Whitelist allowed modules before evaluation
ALLOWED_MODULES = {'math', 'datetime', 'json'}

def eval_custom_component_code(code: str):
    # Validate imports against whitelist
    if not validate_imports(code, ALLOWED_MODULES):
        raise SecurityError("Unauthorized module import detected")
    
    # Generate secure hash to prevent spoofing
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    
    # Evaluate in restricted environment
    return safe_eval(code, restricted_globals)

# Clear credentials after setup
finally:
    # Scrub credentials from in-memory settings after setup
    # Prevents users from gaining access to admin credentials by accessing environment variables
    settings_service.auth_settings.reset_credentials()
```

This prevents attackers from injecting malicious code, accessing unauthorized modules, or exploiting credential exposure vulnerabilities.