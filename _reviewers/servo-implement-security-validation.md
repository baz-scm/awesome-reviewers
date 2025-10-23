---
title: implement security validation
description: Ensure all security-related functionality includes complete validation
  checks and proper testing. This applies to both cryptographic operations and security
  policy configurations.
repository: servo/servo
label: Security
language: Other
comments_count: 2
repository_stars: 32962
---

Ensure all security-related functionality includes complete validation checks and proper testing. This applies to both cryptographic operations and security policy configurations.

For cryptographic operations, implement all required validation steps as specified in standards. For example, in EdDSA signature verification:

```javascript
// Step 2: Validate key data
if (key.representsInvalidPoint() || key.isSmallOrderElement()) {
    return false;
}

// Step 3: Validate signature point R  
if (signatureR.representsInvalidPoint() || signatureR.isSmallOrderElement()) {
    return false;
}
```

For security policies like Content Security Policy, ensure all required directives are properly configured and tested:

```html
<!-- Ensure all necessary permissions are included -->
Content-Security-Policy: sandbox allow-forms allow-scripts
```

Always verify that security validation logic is complete by checking against specifications and testing edge cases. Missing validation steps can create security vulnerabilities, whether in cryptographic implementations or policy configurations.