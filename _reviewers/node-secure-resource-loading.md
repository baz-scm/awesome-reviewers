---
title: Secure resource loading
description: 'Always validate and securely load external resources like libraries,
  configuration files, and modules to prevent tampering and hijacking attacks. When
  implementing security features that depend on system components:'
repository: nodejs/node
label: Security
language: Other
comments_count: 2
repository_stars: 112178
---

Always validate and securely load external resources like libraries, configuration files, and modules to prevent tampering and hijacking attacks. When implementing security features that depend on system components:

1. Use absolute paths rather than relative paths when loading system libraries or resources
2. Verify that critical components are loaded from trusted locations
3. Implement appropriate fallback mechanisms for environments that may not support certain security features
4. Consider platform compatibility and minimum version requirements for security APIs

**Example:**
```cpp
// Secure approach - use absolute paths and verify library existence
HMODULE security_module = LoadLibraryExA(
    "C:\\Windows\\System32\\wldp.dll",  // Use absolute path
    NULL, 
    LOAD_LIBRARY_SEARCH_SYSTEM32);      // Restrict search to system directory

// Check if module is available before using its functions
if (security_module != NULL) {
  // Feature is supported, load function pointers
  pfnSecurityFunction = GetProcAddress(security_module, "SecurityFunction");
  if (pfnSecurityFunction != NULL) {
    // Use security feature
  } else {
    // Handle missing function with appropriate fallback
  }
} else {
  // Module not available, implement secure fallback behavior
}
```

This approach helps prevent attackers from exploiting search path vulnerabilities to load malicious libraries or resources, which could lead to code execution or privilege escalation attacks.