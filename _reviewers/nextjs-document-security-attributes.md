---
title: "Document security attributes"
description: "When handling security-related attributes (like nonces, integrity hashes, or CSP directives), always document the logic and prioritize explicitly passed values over automatically provided ones."
repository: "vercel/next.js"
label: "Security"
language: "TSX"
comments_count: 1
repository_stars: 133000
---

When handling security-related attributes (like nonces, integrity hashes, or CSP directives), always document the logic and prioritize explicitly passed values over automatically provided ones. This ensures that security intentions are clear and that developers can override default security configurations when necessary.

Example:
```javascript
// Get default security attributes from context
let { nonce } = useContext(SecurityContext)

// If a nonce is explicitly passed to the component, favor that over the automatic handling
nonce = props.nonce || nonce
```

This pattern makes security behaviors predictable and allows for custom security requirements while maintaining a secure default implementation.