---
title: Use optional chaining
description: Always use optional chaining (`?.`) and null checks when accessing properties
  or methods on objects that might be null or undefined. This prevents runtime crashes
  and makes code more robust.
repository: snyk/cli
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 5178
---

Always use optional chaining (`?.`) and null checks when accessing properties or methods on objects that might be null or undefined. This prevents runtime crashes and makes code more robust.

Before accessing properties, especially on objects from external sources, API responses, or optional parameters, check for null/undefined values or use optional chaining to safely navigate object properties.

**Examples of unsafe access:**
```typescript
// Unsafe - can crash if vulnerabilities is null
if (jsonData.vulnerabilities.length === 0) { ... }

// Unsafe - can crash if vuln.cvssScore is null  
'security-severity': vuln.cvssScore // pushes "undefined" if null

// Unsafe - can crash if nodes is undefined
for (let i = 0; i < attributes?.dep_graph_data?.graph?.nodes.length; i++) { ... }
```

**Safe alternatives:**
```typescript
// Safe with optional chaining
if (jsonData.vulnerabilities?.length === 0) { ... }

// Safe with null check and conversion
'security-severity': vuln.cvssScore ? String(vuln.cvssScore) : undefined

// Safe with fallback value
const nodes = attributes?.dep_graph_data?.graph?.nodes || [];
for (let i = 0; i < nodes.length; i++) { ... }

// Safe with explicit null check
if (upgradePath && upgradePath.length >= 2) { ... }
```

This pattern is especially critical when the absence of null checks can cause the application to "choke" or crash, as seen with CLI tools processing external data.