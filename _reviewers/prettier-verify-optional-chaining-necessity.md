---
title: Verify optional chaining necessity
description: Analyze whether optional chaining (`?.`) is actually needed based on
  the surrounding context and prior validations. Remove optional chaining when values
  are already confirmed to be truthy through previous checks, but add it when there's
  genuine risk of null/undefined access.
repository: prettier/prettier
label: Null Handling
language: JavaScript
comments_count: 6
repository_stars: 50772
---

Analyze whether optional chaining (`?.`) is actually needed based on the surrounding context and prior validations. Remove optional chaining when values are already confirmed to be truthy through previous checks, but add it when there's genuine risk of null/undefined access.

**Remove when redundant:**
```javascript
// Bad: unnecessary after null check
if (!adjacentNodes.previous || !adjacentNodes.next) {
  return true;
}
const previousKind = adjacentNodes.previous?.kind; // redundant ?. 
const nextKind = adjacentNodes.next?.kind; // redundant ?.

// Good: direct access after validation
if (!adjacentNodes.previous || !adjacentNodes.next) {
  return true;
}
const previousKind = adjacentNodes.previous.kind;
const nextKind = adjacentNodes.next.kind;
```

**Add when necessary:**
```javascript
// Bad: potential exception
return node.groups[0].value === "url";

// Good: safe access
return node.groups?.[0].value === "url";
```

Before using optional chaining, verify: 1) Is there a genuine possibility the value could be null/undefined? 2) Have you already validated the value exists in prior code? 3) Are you mimicking existing safe patterns in the codebase? This prevents both unnecessary defensive coding and potential runtime exceptions.