---
title: use consistent JavaScript syntax
description: Maintain consistent use of modern JavaScript syntax throughout networking
  code to improve reliability and maintainability. Use `const` or `let` instead of
  `var` for variable declarations, and prefer strict equality (`===`) over loose equality
  (`==`) for comparisons.
repository: semgrep/semgrep
label: Networking
language: JavaScript
comments_count: 2
repository_stars: 12598
---

Maintain consistent use of modern JavaScript syntax throughout networking code to improve reliability and maintainability. Use `const` or `let` instead of `var` for variable declarations, and prefer strict equality (`===`) over loose equality (`==`) for comparisons.

This is particularly important in networking code where subtle bugs from variable scoping issues or type coercion can cause runtime errors that are difficult to debug. Consistent syntax also makes the codebase more predictable for team members.

Examples:
```javascript
// Preferred
const proxy = process.env[ssl ? "HTTPS_PROXY" : "HTTP_PROXY"];
if (globalThis.process.platform === "win32" && path === "NUL") {

// Avoid  
var proxy = process.env[ssl ? "HTTPS_PROXY" : "HTTP_PROXY"];
if (globalThis.process.platform === "win32" && path == "NUL") {
```