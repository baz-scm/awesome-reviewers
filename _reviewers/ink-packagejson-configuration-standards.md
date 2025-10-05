---
title: Package.json configuration standards
description: Ensure package.json follows modern standards and maintains consistency
  across configuration fields. Use structured exports instead of simple main field,
  align dependency versions with engine requirements, prefer configuration properties
  over CLI flags, and avoid accidental version locking.
repository: vadimdemedes/ink
label: Configurations
language: Json
comments_count: 4
repository_stars: 31825
---

Ensure package.json follows modern standards and maintains consistency across configuration fields. Use structured exports instead of simple main field, align dependency versions with engine requirements, prefer configuration properties over CLI flags, and avoid accidental version locking.

Key practices:
- Use structured exports with explicit types and default fields:
```json
"exports": {
  "types": "./build/index.d.ts", 
  "default": "./build/index.js"
}
```
- Align @types/node version with engines field (e.g., if engines specifies "node": ">=10", use "@types/node": "^10.17.26")
- Place build tool configuration in package.json properties rather than CLI flags where possible
- Use caret (^) prefixes for dependencies unless intentionally locking versions
- Ensure consistency between related fields like main/exports and engines/type dependencies